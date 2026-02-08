"""Player entity for Cavern game."""
from src.entities.base import GravityActor
from src.constants import WIDTH, HEIGHT


class Player(GravityActor):
    """Player character."""
    
    def __init__(self):
        super().__init__((0, 0))
        self.lives = 2
        self.score = 0
        self.reset()
    
    def reset(self):
        """Reset player state for new life."""
        self.pos = (WIDTH / 2, 100)
        self.vel_y = 0
        self.direction_x = 1  # -1 = left, 1 = right
        self.fire_timer = 0
        self.hurt_timer = 100  # Invulnerable for this many frames
        self.health = 3
        self.blowing_orb = None
    
    def hit_test(self, other):
        """
        Check for collision with bolt.
        
        Returns:
            True if hit and damage taken, False otherwise
        """
        if self.collidepoint(other.pos) and self.hurt_timer < 0:
            # Player loses 1 health, is knocked back, and becomes invulnerable
            self.hurt_timer = 200
            self.health -= 1
            self.vel_y = -12
            self.landed = False
            self.direction_x = other.direction_x
            return True
        return False
    
    def update(self, input_state, grid, game_timer, orbs, play_sound_callback):
        """
        Update player state.
        
        Args:
            input_state: InputState object with current input
            grid: Level grid for collision detection
            game_timer: Current game timer
            orbs: List of active orbs
            play_sound_callback: Function to call for sound effects
        """
        # Apply gravity (disable collision if health is 0)
        self.update_gravity(grid, self.health > 0)
        
        self.fire_timer -= 1
        self.hurt_timer -= 1
        
        if self.landed:
            # Reduce hurt timer once landed
            self.hurt_timer = min(self.hurt_timer, 100)
        
        if self.hurt_timer > 100:
            # Just been hurt - handle knockback or death fall
            if self.health > 0:
                self.move(self.direction_x, 0, 4, grid)
            else:
                if self.top >= HEIGHT * 1.5:
                    # Respawn after falling off screen
                    self.lives -= 1
                    self.reset()
        else:
            # Not hurt - handle normal controls
            self._handle_movement(input_state, grid)
            self._handle_firing(input_state, orbs, play_sound_callback)
            self._handle_jumping(input_state, play_sound_callback)
        
        # Update sprite
        self._update_sprite(input_state, game_timer)
    
    def _handle_movement(self, input_state, grid):
        """Handle horizontal movement."""
        dx = 0
        if input_state.left:
            dx = -1
        elif input_state.right:
            dx = 1
        
        if dx != 0:
            self.direction_x = dx
            # Only move if not firing
            if self.fire_timer < 10:
                self.move(dx, 0, 4, grid)
    
    def _handle_firing(self, input_state, orbs, play_sound_callback):
        """Handle orb creation and blowing."""
        from src.entities.orb import Orb
        
        # Create new orb if conditions are met
        if input_state.fire_pressed and self.fire_timer <= 0 and len(orbs) < 5:
            x = min(730, max(70, self.x + self.direction_x * 38))
            y = self.y - 35
            new_orb = Orb((x, y), self.direction_x)
            orbs.append(new_orb)
            self.blowing_orb = new_orb
            play_sound_callback("blow", 4)
            self.fire_timer = 20
        
        # Blow orb further while holding fire button
        if input_state.fire_held:
            if self.blowing_orb:
                self.blowing_orb.blown_frames += 4
                if self.blowing_orb.blown_frames >= 120:
                    self.blowing_orb = None
        else:
            self.blowing_orb = None
    
    def _handle_jumping(self, input_state, play_sound_callback):
        """Handle jumping."""
        if input_state.up and self.vel_y == 0 and self.landed:
            self.vel_y = -16
            self.landed = False
            play_sound_callback("jump")
    
    def _update_sprite(self, input_state, game_timer):
        """Update sprite based on current state."""
        self.image = "blank"
        
        # Flash when hurt
        if self.hurt_timer <= 0 or self.hurt_timer % 2 == 1:
            dir_index = "1" if self.direction_x > 0 else "0"
            
            if self.hurt_timer > 100:
                # Hurt animation
                if self.health > 0:
                    self.image = "recoil" + dir_index
                else:
                    self.image = "fall" + str((game_timer // 4) % 2)
            elif self.fire_timer > 0:
                # Blowing animation
                self.image = "blow" + dir_index
            elif not input_state.left and not input_state.right:
                # Standing still
                self.image = "still"
            else:
                # Running animation
                self.image = "run" + dir_index + str((game_timer // 8) % 4)
