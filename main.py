from src.engine import Game 
import pygame
import sys

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Game crashed with the following error: {e}")
        pygame.quit()
        sys.exit()