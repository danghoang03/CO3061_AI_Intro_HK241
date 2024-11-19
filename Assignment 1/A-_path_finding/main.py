import pygame
from src.game import Game
from src.utils import read_map_size

def main():
    pygame.display.init()
    pygame.font.init()
    game = Game()
    game.loop()
    
if __name__ == "__main__":
    main()
