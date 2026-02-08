"""Game Over screen for Cavern game."""
from src.utils import draw_text
from src.constants import WIDTH, IMAGE_WIDTH, CHAR_WIDTH


class GameOverScreen:
    """Game over screen."""
    
    def __init__(self, final_score, final_level):
        self.final_score = final_score
        self.final_level = final_level
    
    def update(self, input_state, play_sound_callback):
        """
        Update game over screen.
        
        Returns:
            Next screen to transition to, or None to stay on game over
        """
        if input_state.fire_pressed:
            # Return to menu
            from src.screens.menu import MenuScreen
            return MenuScreen()
        
        return None
    
    def draw(self, screen):
        """Draw game over screen."""
        # Draw black background (or use a game over background)
        screen.fill((0, 0, 0))
        
        # Draw "Game Over" image
        screen.blit("over", (0, 0))
        
        # Display final score (right-justified)
        number_width = CHAR_WIDTH[0]
        score_str = str(self.final_score)
        draw_text(screen, score_str, 451, WIDTH - 2 - (number_width * len(score_str)))
        
        # Display final level
        draw_text(screen, "LEVEL " + str(self.final_level), 451)
