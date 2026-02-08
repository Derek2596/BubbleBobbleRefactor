"""Base actor classes for Cavern game."""
from pgzero.actor import Actor
from src.constants import ANCHOR_CENTRE, ANCHOR_CENTRE_BOTTOM, HEIGHT, GRID_BLOCK_SIZE
from src.utils import block, sign


class CollideActor(Actor):
    """Actor with collision detection against level blocks."""
    
    def __init__(self, pos, anchor=ANCHOR_CENTRE):
        super().__init__("blank", pos, anchor)
    
    def move(self, dx, dy, speed, grid):
        """
        Move actor with collision detection.
        
        Returns:
            True if collided with block or edge, False otherwise
        """
        new_x, new_y = int(self.x), int(self.y)
        
        # Movement is done 1 pixel at a time to avoid embedding into walls
        for i in range(speed):
            new_x, new_y = new_x + dx, new_y + dy
            
            if new_x < 70 or new_x > 730:
                # Collided with edge of level
                return True
            
            # Check for block collision
            if ((dy > 0 and new_y % GRID_BLOCK_SIZE == 0 or
                 dx > 0 and new_x % GRID_BLOCK_SIZE == 0 or
                 dx < 0 and new_x % GRID_BLOCK_SIZE == GRID_BLOCK_SIZE - 1)
                and block(new_x, new_y, grid)):
                return True
            
            # Update position if no collision
            self.pos = new_x, new_y
        
        # Didn't collide
        return False


class GravityActor(CollideActor):
    """Actor affected by gravity."""
    
    MAX_FALL_SPEED = 10
    
    def __init__(self, pos):
        super().__init__(pos, ANCHOR_CENTRE_BOTTOM)
        self.vel_y = 0
        self.landed = False
    
    def update_gravity(self, grid, detect=True):
        """Apply gravity and handle falling."""
        # Apply gravity without exceeding max fall speed
        self.vel_y = min(self.vel_y + 1, GravityActor.MAX_FALL_SPEED)
        
        if detect:
            # Move vertically with collision detection
            if self.move(0, sign(self.vel_y), abs(self.vel_y), grid):
                # Landed on a block
                self.vel_y = 0
                self.landed = True
            
            if self.top >= HEIGHT:
                # Fallen off bottom - reappear at top
                self.y = 1
        else:
            # No collision detection - just update Y
            self.y += self.vel_y
