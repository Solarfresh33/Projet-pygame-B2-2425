import pygame
import pytmx

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 800:  # Si l'étoile sort de l'écran, elle est supprimée
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tmx_file):
        super().__init__()
        # Chargement de l'image du joueur
        try:
            self.image = pygame.image.load("assets/kirby.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
        except pygame.error as e:
            print(f"Couldn't load player image: {e}")
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 20, 147))  # Couleur par défaut

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Mouvement
        self.velocity_y = 0
        self.gravity = 0.7
        self.jump_speed = -15
        self.speed = 2
        self.health = 3
        self.can_jump = True
        self.invincible = False

        # Groupe pour les étoiles
        self.stars = pygame.sprite.Group()

        # Chargement de la tuile de l'étoile depuis le fichier TMX
        self.star_image = self.load_star_image(tmx_file)

    def load_star_image(self, tmx_file):
        """Charge l'image de l'étoile à partir du fichier TMX."""
        tmx_data = pytmx.load_pygame(tmx_file)
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:  # Vérifie si une tuile correspond
                        return pygame.transform.scale(tile, (20, 20))
        print("Star image not found in TMX file.")
        return pygame.Surface((20, 20))  # Tuile par défaut si introuvable

    def update(self):
        # Gravité
        self.velocity_y += self.gravity

        # Entrées clavier
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_jump:
            self.jump()
        if keys[pygame.K_x]:  # Lancer une étoile
            self.attack()

        # Mise à jour des étoiles
        self.stars.update()

    def jump(self):
        self.velocity_y = self.jump_speed
        self.can_jump = False

    def attack(self):
        """Lancer une étoile depuis la position actuelle de Kirby."""
        star = Star(self.rect.centerx, self.rect.centery, self.star_image)
        self.stars.add(star)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.stars.draw(surface)
