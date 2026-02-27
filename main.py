"""
main.py
The entry point of the Pokémon Adventure application. 
Responsible for initializing the game engine and handling top-level crashes.
"""

from src.engine import Game 
import pygame
import sys

def main():
    """
    Instantiates the Game engine and starts the main loop.
    This keeps the global namespace clean and follows best practices.
    """
    game=Game()
    game.run()

if __name__=="__main__":
    # The guard clause ensures the game only runs when this script is executed directly.
    try:
        main()
    except Exception as e:
        # Global Error Handling: Prevents the window from hanging in case of a crash.
        print(f"Game crashed with the following error: {e}")
        pygame.quit()
        sys.exit()