"""Orb entity for Cavern game."""
from random import randint
from src.entities.base import CollideActor
from src.constants import ANCHOR_CENTRE


class Orb(CollideActor):
    """Bubble that can trap enemies."""
    
    MAX_TIMER = 250
    
    def __init__(self, pos, dir_x):
        super().__init__(pos, ANCHOR_CENTRE)
        self.direction_x = dir_x
        self.floating = False
        self.trapped_enemy_type = None
        self.timer = -1
        self.blown_frames = 6
    
    def hit_test(self, bolt):
        """Check for collision with a bolt."""
        collided = self.collidepoint(bolt.pos)
        if collided:
            self.timer = Orb.MAX_TIMER - 1
        return collided
    
    def update(self, grid, pops, fruits, play_sound_callback):
        """Update orb state."""
        self.timer += 1
        
        if self.floating:
            # Float upwards
            self.move(0, -1, randint(1, 2), grid)
        else:
            # Move horizontally
            if self.move(self.direction_x, 0, 4, grid):
                # Hit a block - start floating
                self.floating = True
        
        if self.timer == self.blown_frames:
            self.floating = True
        elif self.timer >= Orb.MAX_TIMER or self.y <= -40:
            # Pop if lifetime expired or off screen
            from src.entities.effects import Pop
            from src.entities.fruit import Fruit
            
            pops.append(Pop(self.pos, 1))
            if self.trapped_enemy_type is not None:
                fruits.append(Fruit(self.pos, self.trapped_enemy_type))
            play_sound_callback("pop", 4)
        
        # Update sprite
        if self.timer < 9:
            # Growing animation
            self.image = "orb" + str(self.timer // 3)
        else:
            if self.trapped_enemy_type is not None:
                # Trapped enemy animation
                self.image = "trap" + str(self.trapped_enemy_type) + str((self.timer // 4) % 8)
            else:
                # Normal orb animation
                self.image = "orb" + str(3 + (((self.timer - 9) // 8) % 4))
