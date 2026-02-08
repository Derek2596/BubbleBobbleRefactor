"""Core game logic for Cavern."""
from random import randint, shuffle
from src.constants import LEVELS, NUM_COLUMNS, GRID_BLOCK_SIZE, LEVEL_X_OFFSET, WIDTH, NUM_ROWS
from src.entities.robot import Robot
from src.entities.fruit import Fruit


class Game:
    """Core game state and logic."""
    
    def __init__(self, player=None):
        self.player = player
        self.level_colour = 0  # Start at 0 for valid background image
        self.level = 0  # Start at 0 instead of -1
        self.timer = -1
        
        # Initialize grid properly
        level_data = LEVELS[0]
        self.grid = level_data + [level_data[0]]  # Add last row
        
        # Entity lists
        self.fruits = []
        self.bolts = []
        self.enemies = []
        self.pops = []
        self.orbs = []
        self.pending_enemies = []
        
        if player:
            # Reset to -1 so next_level() will increment to 0
            self.level_colour = -1
            self.level = -1
            self.next_level()
    
    def next_level(self):
        """Progress to next level."""
        self.level_colour = (self.level_colour + 1) % 4
        self.level += 1
        
        # Set up grid
        self.grid = LEVELS[self.level % len(LEVELS)]
        self.grid = self.grid + [self.grid[0]]  # Add last row
        
        self.timer = -1
        
        if self.player:
            self.player.reset()
        
        # Reset entity lists
        self.fruits = []
        self.bolts = []
        self.enemies = []
        self.pops = []
        self.orbs = []
        
        # Create pending enemies
        num_enemies = 10 + self.level
        num_strong_enemies = 1 + int(self.level / 1.5)
        num_weak_enemies = num_enemies - num_strong_enemies
        
        self.pending_enemies = (num_strong_enemies * [Robot.TYPE_AGGRESSIVE] + 
                               num_weak_enemies * [Robot.TYPE_NORMAL])
        shuffle(self.pending_enemies)
    
    def fire_probability(self):
        """Calculate enemy firing probability based on level."""
        return 0.001 + (0.0001 * min(100, self.level))
    
    def max_enemies(self):
        """Calculate max simultaneous enemies based on level."""
        return min((self.level + 6) // 2, 8)
    
    def get_robot_spawn_x(self):
        """Find spawn location for robot."""
        r = randint(0, NUM_COLUMNS - 1)
        
        for i in range(NUM_COLUMNS):
            grid_x = (r + i) % NUM_COLUMNS
            if self.grid[0][grid_x] == ' ':
                return GRID_BLOCK_SIZE * grid_x + LEVEL_X_OFFSET + 12
        
        return WIDTH / 2
    
    def update(self, input_state, play_sound_callback):
        """
        Update game state.
        
        Args:
            input_state: InputState object
            play_sound_callback: Function to call for sound effects
        """
        self.timer += 1
        
        # Update player
        if self.player:
            self.player.update(input_state, self.grid, self.timer, self.orbs, play_sound_callback)
        
        # Update all entities
        for fruit in self.fruits:
            fruit.update(self.grid, self.player, self.pops, self.timer, play_sound_callback)
        
        for bolt in self.bolts:
            bolt.update(self.grid, self.orbs, self.player, self.timer)
        
        for enemy in self.enemies:
            enemy.update(self.grid, self.player, self.orbs, self.bolts, 
                        self.timer, self.fire_probability(), play_sound_callback)
        
        for pop in self.pops:
            pop.update()
        
        for orb in self.orbs:
            orb.update(self.grid, self.pops, self.fruits, play_sound_callback)
        
        # Remove inactive entities
        self.fruits = [f for f in self.fruits if f.time_to_live > 0]
        self.bolts = [b for b in self.bolts if b.active]
        self.enemies = [e for e in self.enemies if e.alive]
        self.pops = [p for p in self.pops if p.timer < 12]
        self.orbs = [o for o in self.orbs if o.timer < 250 and o.y > -40]
        
        # Spawn random fruit
        if self.timer % 100 == 0 and len(self.pending_enemies + self.enemies) > 0:
            self.fruits.append(Fruit((randint(70, 730), randint(75, 400))))
        
        # Spawn enemies
        if (self.timer % 81 == 0 and len(self.pending_enemies) > 0 and 
            len(self.enemies) < self.max_enemies()):
            robot_type = self.pending_enemies.pop()
            pos = (self.get_robot_spawn_x(), -30)
            self.enemies.append(Robot(pos, robot_type))
        
        # Check for level completion
        if len(self.pending_enemies + self.fruits + self.enemies + self.pops) == 0:
            if len([orb for orb in self.orbs if orb.trapped_enemy_type is not None]) == 0:
                self.next_level()
                play_sound_callback("level", 1)
    
    def draw(self, screen):
        """Draw game state."""
        # Draw background
        screen.blit("bg%d" % self.level_colour, (0, 0))
        
        # Draw blocks
        block_sprite = "block" + str(self.level % 4)
        for row_y in range(NUM_ROWS):
            row = self.grid[row_y]
            if len(row) > 0:
                x = LEVEL_X_OFFSET
                for block_char in row:
                    if block_char != ' ':
                        screen.blit(block_sprite, (x, row_y * GRID_BLOCK_SIZE))
                    x += GRID_BLOCK_SIZE
        
        # Draw all entities
        all_objs = self.fruits + self.bolts + self.enemies + self.pops + self.orbs
        if self.player:
            all_objs.append(self.player)
        
        for obj in all_objs:
            if obj:
                obj.draw()