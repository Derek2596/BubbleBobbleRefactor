"""Fruit pickup entity for Cavern game."""
from random import choice
from src.entities.base import GravityActor


class Fruit(GravityActor):
    """Pickup items including fruit and powerups."""
    
    APPLE = 0
    RASPBERRY = 1
    LEMON = 2
    EXTRA_HEALTH = 3
    EXTRA_LIFE = 4
    
    def __init__(self, pos, trapped_enemy_type=0):
        super().__init__(pos)
        
        # Choose fruit type based on enemy type
        if trapped_enemy_type == 0:  # Normal enemy
            self.type = choice([Fruit.APPLE, Fruit.RASPBERRY, Fruit.LEMON])
        else:  # Aggressive enemy - chance for powerups
            types = 10 * [Fruit.APPLE, Fruit.RASPBERRY, Fruit.LEMON]
            types += 9 * [Fruit.EXTRA_HEALTH]
            types += [Fruit.EXTRA_LIFE]
            self.type = choice(types)
        
        self.time_to_live = 500
    
    def update(self, grid, player, pops, game_timer, play_sound_callback):
        """Update fruit state."""
        self.update_gravity(grid)
        
        # Check collision with player
        if player and player.collidepoint(self.center):
            if self.type == Fruit.EXTRA_HEALTH:
                player.health = min(3, player.health + 1)
                play_sound_callback("bonus")
            elif self.type == Fruit.EXTRA_LIFE:
                player.lives += 1
                play_sound_callback("bonus")
            else:
                player.score += (self.type + 1) * 100
                play_sound_callback("score")
            
            self.time_to_live = 0
        else:
            self.time_to_live -= 1
        
        if self.time_to_live <= 0:
            # Create pop animation
            from src.entities.effects import Pop
            pops.append(Pop((self.x, self.y - 27), 0))
        
        # Update sprite
        anim_frame = str([0, 1, 2, 1][(game_timer // 6) % 4])
        self.image = "fruit" + str(self.type) + anim_frame
