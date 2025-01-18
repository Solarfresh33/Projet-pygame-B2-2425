import pygame
import sys
from button import Button
# Initialisation de Pygame
pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        # Dimensions de la fenêtre
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Déplacement du personnage avec saut - ZQSD")

        # Couleurs
        WHITE = (255, 255, 255)
        BLUE = (0, 0, 255)

        # Variables du personnage
        player_width, player_height = 50, 50
        player_x, player_y = WIDTH // 2, HEIGHT - player_height
        player_speed = 5

        # Variables pour le saut
        is_jumping = False
        jump_velocity = 15  # Vitesse initiale du saut
        gravity = 1  # Gravité qui ramène le joueur vers le sol
        velocity_y = 0  # Vitesse verticale
        ground_level = HEIGHT - player_height  # Niveau du sol

        # Boucle principale
        running = True
        while running:
            # Gestion des événements
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Détecter les touches appuyées
            keys = pygame.key.get_pressed()

            # Déplacement horizontal avec Q et D
            if keys[pygame.K_q]:  # Gauche
                player_x -= player_speed
            if keys[pygame.K_d]:  # Droite
                player_x += player_speed

            # Gestion du saut avec Space
            if not is_jumping and keys[pygame.K_SPACE]:
                is_jumping = True
                velocity_y = -jump_velocity

            # Gestion de la gravité et du saut
            if is_jumping:
                player_y += velocity_y  # Appliquer la vitesse verticale
                velocity_y += gravity  # Appliquer la gravité

            # Vérifier si le joueur touche le sol
            if player_y >= ground_level:
                player_y = ground_level
                is_jumping = False

            # Dessiner sur l'écran
            screen.fill(WHITE)  # Effacer l'écran avec du blanc
            pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))  # Dessiner le personnage
            pygame.display.flip()  # Mettre à jour l'affichage

            # Contrôler la fréquence d'image
            pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()