import pygame

# Initialisation de Pygame
pygame.init()

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

# Quitter Pygame
pygame.quit()
