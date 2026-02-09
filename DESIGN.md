# Design Document

## Screens Architecture

The game uses the **State Pattern** to manage different game states (menu, play, game over).

### Components
- **App** (`src/app.py`): Owns the current screen, delegates update/draw calls, handles screen transitions
- **Screen Interface**: Each screen implements:
  - `update(input_state, play_sound_callback) -> Screen | None`: Updates state, returns next screen or None
  - `draw(screen)`: Renders to the screen

### Screen Lifecycle
```
MenuScreen
    ↓ (SPACE pressed)
PlayScreen
    ↓ (player dies)
GameOverScreen
    ↓ (SPACE pressed)
MenuScreen (loop)
```

### Benefits
- No global state enum (`State.MENU`, `State.PLAY`, etc.)
- Each screen encapsulates its own logic
- Easy to add new screens (settings, high scores)
- Screen transitions are explicit and clear

## Input Design

The game uses the **Command Pattern** for input handling with centralized edge detection.

### Components
- **InputState** (`src/input.py`): Immutable snapshot of input for one frame
  - `left`, `right`, `up`: Direction buttons (level)
  - `fire_pressed`: Create orb (edge-detected)
  - `fire_held`: Blow orb further (level)
  - `pause_pressed`: Toggle pause (edge-detected)

- **InputManager** (`src/input.py`): Tracks previous frame state to detect edges
  - `get_input_state(keyboard) -> InputState`: Builds snapshot with edge detection

### Flow
```
keyboard (Pygame Zero builtin)
    ↓
InputManager.get_input_state()
    ↓
InputState (immutable)
    ↓
Player.update(input_state, ...)
```

### Benefits
- No global `space_down` variable
- Entities don't access `keyboard` directly
- Input can be recorded/replayed for testing
- Edge detection centralized in one place

## Pause System

Pause is implemented entirely within **PlayScreen** without affecting other states.

### Implementation
```python
class PlayScreen:
    def __init__(self):
        self.game = Game(Player())
        self.paused = False
    
    def update(self, input_state, play_sound_callback):
        # Toggle pause
        if input_state.pause_pressed:
            self.paused = not self.paused
            return None
        
        # Skip game update if paused
        if self.paused:
            return None
        
        # Normal update
        self.game.update(input_state, play_sound_callback)
        return None
    
    def draw(self, screen):
        # Always draw game state
        self.game.draw(screen)
        
        # Overlay if paused
        if self.paused:
            draw_text(screen, "PAUSED", 200)
```

### Key Points
- Pause flag is local to `PlayScreen`
- Game simulation completely frozen when paused
- Screen still renders (shows frozen game + overlay)
- Menu and GameOver screens ignore pause input
- Clean resume - no state corruption

### Benefits
- Simple implementation (just a boolean flag)
- No global pause state
- Contained within the screen that needs it
- Easy to extend (pause menu, settings)