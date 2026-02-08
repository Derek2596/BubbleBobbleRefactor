"""Main application class for Cavern game."""
from src.input import InputManager
from src.screens.menu import MenuScreen


class App:
    """Main application that manages screens and game flow."""
    
    def __init__(self, play_sound_callback):
        self.current_screen = MenuScreen()
        self.input_manager = InputManager()
        self.play_sound_callback = play_sound_callback
    
    def change_screen(self, new_screen):
        """Change to a new screen."""
        if new_screen is not None:
            self.current_screen = new_screen
    
    def update(self, keyboard):
        """
        Update current screen.
        
        Args:
            keyboard: Pygame Zero keyboard object
        """
        # Get input state for this frame
        input_state = self.input_manager.get_input_state(keyboard)
        
        # Update current screen and handle screen transitions
        next_screen = self.current_screen.update(input_state, self.play_sound_callback)
        self.change_screen(next_screen)
    
    def draw(self, screen):
        """
        Draw current screen.
        
        Args:
            screen: Pygame Zero screen object
        """
        self.current_screen.draw(screen)
