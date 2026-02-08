"""Sound management for Cavern game."""
from random import randint


class SoundManager:
    """Manages game sound effects and music."""
    
    def __init__(self, sounds_module):
        """
        Initialize sound manager.
        
        Args:
            sounds_module: Pygame Zero sounds module
        """
        self.sounds = sounds_module
    
    def play_sound(self, name, count=1):
        """
        Play a sound effect.
        
        Args:
            name: Base name of sound file
            count: Number of variants (will randomly choose one)
        """
        try:
            sound_name = name + str(randint(0, count - 1))
            sound = getattr(self.sounds, sound_name)
            sound.play()
        except Exception as e:
            # Silently ignore missing sounds
            print(f"Sound not found: {e}")
