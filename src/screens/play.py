"""Play screen for Cavern game."""
from src.game import Game
from src.entities.player import Player
from src.utils import draw_text
from src.constants import WIDTH, IMAGE_WIDTH, CHAR_WIDTH


class PlayScreen:
    """Main gameplay screen."""
    
    def __init__(self):
        self.game = Game(Player())
        self.paused = False
    
    def update(self, input_state, play_sound_callback):
        """
        Update play screen.
        
        Returns:
            Next screen to transition to, or None to continue playing
        """
        # Handle pause toggle
        if input_state.pause_pressed:
            self.paused = not self.paused
            return None
        
        # Don't update game if paused
        if self.paused:
            return None
        
        # Check for game over
        if self.game.player.lives < 0:
            play_sound_callback("over")
            from src.screens.game_over import GameOverScreen
            return GameOverScreen(self.game.player.score, self.game.level + 1)
        
        # Update game
        self.game.update(input_state, play_sound_callback)
        
        return None
    
    def draw(self, screen):
        """Draw play screen."""
        # Draw game
        self.game.draw(screen)
        
        # Draw HUD
        self._draw_status(screen)
        
        # Draw pause overlay if paused
        if self.paused:
            self._draw_pause_overlay(screen)
    
    def _draw_status(self, screen):
        """Draw status bar with score, level, lives, and health."""
        # Display score (right-justified)
        number_width = CHAR_WIDTH[0]
        score_str = str(self.game.player.score)
        draw_text(screen, score_str, 451, WIDTH - 2 - (number_width * len(score_str)))
        
        # Display level number
        draw_text(screen, "LEVEL " + str(self.game.level + 1), 451)
        
        # Display lives and health
        lives_health = ["life"] * min(2, self.game.player.lives)
        if self.game.player.lives > 2:
            lives_health.append("plus")
        if self.game.player.lives >= 0:
            lives_health += ["health"] * self.game.player.health
        
        x = 0
        for image in lives_health:
            screen.blit(image, (x, 450))
            x += IMAGE_WIDTH[image]
    
    def _draw_pause_overlay(self, screen):
        """Draw pause overlay."""
        # Semi-transparent overlay (we'll just draw text for now)
        draw_text(screen, "PAUSED", 200)
        draw_text(screen, "PRESS P TO RESUME", 250)
