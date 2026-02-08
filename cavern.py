"""
Cavern - A Pygame Zero Game (Refactored)

This is a refactored version of the Cavern game that uses:
- Screen objects (State pattern) for menu/play/game over states
- Input snapshot with edge detection (Command pattern)
- Pause functionality
- Improved code organization and maintainability
"""
import sys
import traceback

try:
    import pygame
except ImportError as e:
    print(f"ERROR: Could not import pygame: {e}")
    print("Install with: pip3 install pygame")
    sys.exit(1)

try:
    import pgzero
except ImportError as e:
    print(f"ERROR: Could not import pgzero: {e}")
    print("Install with: pip3 install pgzero")
    sys.exit(1)

try:
    import pgzrun
except ImportError as e:
    print(f"ERROR: Could not import pgzrun: {e}")
    print("Install with: pip3 install pgzero")
    sys.exit(1)

# Check Python version
if sys.version_info < (3, 5):
    print("This game requires at least version 3.5 of Python. Please download it from www.python.org")
    sys.exit()

# Check Pygame Zero version
pgzero_version = [int(s) if s.isnumeric() else s for s in pgzero.__version__.split('.')]
if pgzero_version < [1, 2]:
    print(f"This game requires at least version 1.2 of Pygame Zero. You have version {pgzero.__version__}. "
          f"Please upgrade using the command 'pip3 install --upgrade pgzero'")
    sys.exit()

# Import after version checks
try:
    from src.constants import WIDTH as GAME_WIDTH, HEIGHT as GAME_HEIGHT, TITLE as GAME_TITLE
    
    # Pygame Zero needs these as module-level globals
    WIDTH = GAME_WIDTH
    HEIGHT = GAME_HEIGHT
    TITLE = GAME_TITLE
except ImportError as e:
    print(f"ERROR: Could not import from src.constants: {e}")
    print("Make sure you're running from the cavern_refactored directory")
    print("Current directory should contain: cavern.py and src/ folder")
    traceback.print_exc()
    sys.exit(1)

try:
    from src.app import App
    from src.sound import SoundManager
except ImportError as e:
    print(f"ERROR: Could not import from src: {e}")
    traceback.print_exc()
    sys.exit(1)

# Global app instance
app = None
sound_manager = None


def initialize():
    """Initialize the game."""
    global app, sound_manager
    
    print("Initializing game...")
    
    # Set up sound system
    try:
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 2, 1024)
    except Exception as e:
        # Ignore sound initialization errors
        print(f"Warning: Sound initialization failed: {e}")
        pass
    
    try:
        # sounds and music are injected as builtins by Pygame Zero - just use them directly
        
        # Try to play music
        try:
            music.play("theme")
            music.set_volume(0.3)
            print("Music started")
        except Exception as e:
            print(f"Warning: Could not play music: {e}")
        
        # Create sound manager (sounds is a builtin)
        sound_manager = SoundManager(sounds)
        
        # Create app
        app = App(sound_manager.play_sound)
    except Exception as e:
        print(f"ERROR during initialization: {e}")
        traceback.print_exc()
        raise


def update():
    """Pygame Zero update callback."""
    global app
    try:
        if app is None:
            initialize()
        app.update(keyboard)
    except Exception as e:
        print(f"ERROR in update(): {e}")
        traceback.print_exc()
        raise


def draw():
    """Pygame Zero draw callback."""
    global app
    try:
        if app is None:
            # Don't initialize in draw, wait for update
            screen.fill((0, 0, 0))
            return
        app.draw(screen)
    except Exception as e:
        print(f"ERROR in draw(): {e}")
        traceback.print_exc()
        raise


# Run the game
if __name__ == "__main__":
    try:
        print("Starting Pygame Zero...")
        print("Window should appear...")
        pgzrun.go()
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)