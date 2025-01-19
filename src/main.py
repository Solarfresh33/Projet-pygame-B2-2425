import pygame
from game import Game

# clock = pygame.time.Clock()

# Charge ton niveau
# LEVEL_FILE = "levels/level-1.tmx"

def main():
    pygame.init()  # Initialiser pygame au début
    game = Game()  # Créer une instance de la classe Game
    game.run()  # Lancer la boucle principale du jeu
    pygame.quit()

if __name__ == "__main__":
    main()


