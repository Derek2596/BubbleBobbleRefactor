"""Bolt entity for Cavern game."""
from src.entities.base import CollideActor
from src.constants import ANCHOR_CENTRE


class Bolt(CollideActor):
    """Projectile fired by enemies."""
    
    SPEED = 7
    
    def __init__(self, pos, dir_x):
        super().__init__(pos, ANCHOR_CENTRE)
        self.direction_x = dir_x
        self.active = True
    
    def update(self, grid, orbs, player, game_timer):
        """Update bolt position and check collisions."""
        # Move horizontally and check for block collision
        if self.move(self.direction_x, 0, Bolt.SPEED, grid):
            self.active = False
        else:
            # Check collision with orbs and player
            targets = orbs + ([player] if player else [])
            for obj in targets:
                if obj and obj.hit_test(self):
                    self.active = False
                    break
        
        # Update sprite
        direction_idx = "1" if self.direction_x > 0 else "0"
        anim_frame = str((game_timer // 4) % 2)
        self.image = "bolt" + direction_idx + anim_frame
