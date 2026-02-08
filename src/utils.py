"""Utility functions for Cavern game."""
from src.constants import GRID_BLOCK_SIZE, LEVEL_X_OFFSET, NUM_ROWS, NUM_COLUMNS


def block(x, y, grid):
    """Check if there is a level grid block at these coordinates."""
    grid_x = (x - LEVEL_X_OFFSET) // GRID_BLOCK_SIZE
    grid_y = y // GRID_BLOCK_SIZE
    if grid_y > 0 and grid_y < NUM_ROWS:
        row = grid[grid_y]
        return grid_x >= 0 and grid_x < NUM_COLUMNS and len(row) > 0 and row[grid_x] != " "
    else:
        return False


def sign(x):
    """Return -1 or 1 depending on whether number is positive or negative."""
    return -1 if x < 0 else 1


def char_width(char):
    """Return width of given character in the font."""
    from src.constants import CHAR_WIDTH
    index = max(0, ord(char) - 65)
    return CHAR_WIDTH[index]


def draw_text(screen, text, y, x=None):
    """Draw text on screen using custom font."""
    from src.constants import WIDTH
    
    if x is None:
        # Center text if no X position specified
        x = (WIDTH - sum([char_width(c) for c in text])) // 2
    
    for char in text:
        screen.blit("font0" + str(ord(char)), (x, y))
        x += char_width(char)
