import pygame
from game import Game
from menu import main_menu
from button import Button

# clock = pygame.time.Clock()

# Charge ton niveau
# LEVEL_FILE = "levels/level-1.tmx"

def main():
    pygame.init()  # Initialiser pygame au début
    main_menu()
    pygame.quit()

if __name__ == "__main__":
    main()


