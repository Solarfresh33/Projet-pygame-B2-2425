import pygame
from game import Game

pygame.init()

# clock = pygame.time.Clock()

# Charge ton niveau
# LEVEL_FILE = "levels/level-1.tmx"

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()

