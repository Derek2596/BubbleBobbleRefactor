"""Menu screen for Cavern game."""
from src.game import Game


class MenuScreen:
    """Main menu screen."""
    
    def __init__(self):
        # Create game without player for background animation
        self.game = Game()
    
    def update(self, input_state, play_sound_callback):
        """
        Update menu screen.
        
        Returns:
            Next screen to transition to, or None to stay on menu
        """
        if input_state.fire_pressed:
            # Start new game
            from src.screens.play import PlayScreen
            return PlayScreen()
        
        # Update background game
        from src.input import InputState
        empty_input = InputState(False, False, False, False, False, False, False)
        self.game.update(empty_input, play_sound_callback)
        
        return None
    
    def draw(self, screen):
        """Draw menu screen."""
        # Draw background game
        self.game.draw(screen)
        
        # Draw title
        screen.blit("title", (0, 0))
        
        # Draw "Press SPACE" animation
        anim_frame = min(((self.game.timer + 40) % 160) // 4, 9)
        screen.blit("space" + str(anim_frame), (130, 280))
