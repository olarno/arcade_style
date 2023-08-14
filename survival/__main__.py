import pygame
from game import Survival

def main():
    pygame.init()
    game = Survival()
    game.main_loop()
    pygame.quit()

if __name__ == "__main__":
    main()
