"""Input handling with edge detection for Cavern game."""
from dataclasses import dataclass


@dataclass
class InputState:
    """Snapshot of input state for a single frame."""
    left: bool
    right: bool
    up: bool
    jump_pressed: bool  # Edge-detected
    fire_pressed: bool  # Edge-detected (create orb)
    fire_held: bool     # Level (blow orb further)
    pause_pressed: bool # Edge-detected


class InputManager:
    """Manages input state and edge detection."""
    
    def __init__(self):
        self._space_was_down = False
        self._p_was_down = False
    
    def get_input_state(self, keyboard) -> InputState:
        """
        Build InputState from current keyboard state.
        
        Args:
            keyboard: Pygame Zero keyboard object
            
        Returns:
            InputState snapshot for this frame
        """
        # Edge detection for SPACE
        space_pressed = False
        if keyboard.space:
            if not self._space_was_down:
                space_pressed = True
                self._space_was_down = True
        else:
            self._space_was_down = False
        
        # Edge detection for P (pause)
        p_pressed = False
        if keyboard.p:
            if not self._p_was_down:
                p_pressed = True
                self._p_was_down = True
        else:
            self._p_was_down = False
        
        return InputState(
            left=keyboard.left,
            right=keyboard.right,
            up=keyboard.up,
            jump_pressed=keyboard.up,  # Could add edge detection if needed
            fire_pressed=space_pressed,
            fire_held=keyboard.space,
            pause_pressed=p_pressed
        )
