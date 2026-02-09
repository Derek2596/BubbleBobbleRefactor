## How to run the game

1. Install pygame and pgzero
2. From the root directory (`BubbleBobbleRefactor/`), run: 
```
pgzrun cavern.py
```

### Controls
- **←/→** - Move left/right
- **↑** - Jump
- **SPACE** - Fire orb (tap) / Blow orb further (hold)
- **P** - Pause/Resume

## Architectural changes

This refactor transformed a 1000+ line monolithic script into a modular, maintainable codebase:

### Key Improvements
- **State Pattern**: Replaced global state enum with screen objects (`MenuScreen`, `PlayScreen`, `GameOverScreen`)
- **Command Pattern**: Centralized input handling with `InputState` dataclass and edge detection
- **Dependency Injection**: Entities receive dependencies (input, callbacks) rather than accessing globals
- **Pause System**: Clean pause/resume in `PlayScreen` without affecting other states

### Structure
```
cavern_refactored/
├── cavern.py              # Main entry (~80 lines vs 1000+)
├── src/
│   ├── app.py             # App manages screen lifecycle
│   ├── input.py           # InputManager & InputState
│   ├── game.py            # Core game logic
│   ├── entities/          # Player, Robot, Orb, etc.
│   └── screens/           # Menu, Play, GameOver
└── images/, sounds/, music/  # Assets from original
```
