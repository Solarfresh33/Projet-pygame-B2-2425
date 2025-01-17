import pygame
import time 

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y , extra_arg=None):
        super().__init__()
        self.extra_arg = extra_arg
        # Load and scale the player image
        try:
            # Load the tileset image
            tileset = pygame.image.load("levels/kirby-like.png").convert_alpha()
            self.sprites = []  # Initialiser une liste pour les sprites d'animation
            self.last_update_time = pygame.time.get_ticks()  # Temps du dernier changement de sprite
            self.animation_delay = 300  # Délai entre les animations en millisecondes (1 seconde)
            self.current_sprite = 0
            # Calculate the position of the tile in the tileset
            tile_width = 16
            tile_height = 16
            for tile_number in animation_tiles:
                tile_x = (tile_number % 9) * tile_width
                tile_y = (tile_number // 9) * tile_height

                # Extraire et redimensionner chaque sprite
                sprite = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
                sprite.blit(tileset, (0, 0), (tile_x, tile_y, tile_width, tile_height))
                sprite = pygame.transform.scale(sprite, (30, 30))
                self.sprites.append(sprite)


            self.image = self.sprites[self.current_sprite]
            
            
        except pygame.error as e:
            print(f"Couldn't load enemy image: {e}")
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 0, 0))  # Red fallback color
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)  # Use topleft instead of setting x,y separately
        
        # Movement attributes
        self.velocity_y = 0
        self.gravity = 0.7
        self.jump_speed = -15
        self.speed = 2
        self.health = 3
        self.can_jump = True  # Add this to control jump
        self.invincible = False  # Par défaut, pas invincible
        self.last_attack_time = time.time()  # Stocke le temps actuel (en secondes)
        self.attack_cooldown = 1

        self.stars = pygame.sprite.Group()

    def update(self):
        self.velocity_y += self.gravity

        # Get keyboard input for jumping
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_jump:
            self.jump()
        current_time = time.time()
        if keys[pygame.K_x] and current_time - self.last_attack_time >= self.attack_cooldown:
            self.attack()
            self.last_attack_time = current_time  # Met à jour le temps de la dernière attaque


        # Mise à jour des étoiles
        self.stars.update()

    def jump(self):
        self.velocity_y = self.jump_speed
        self.can_jump = False  # Prevent further jumps until landing 
    
    def attack(self):
        """Lancer une étoile depuis la position actuelle de Kirby."""
        print("Attack triggered!")
        star = Star(self.rect.centerx, self.rect.centery)
        self.stars.add(star)

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # Dessiner Kirby
        self.stars.draw(surface)  # Dessiner les étoiles


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = 4
        tileset = pygame.image.load("levels/kirby-like.png").convert_alpha()
        tile_number=9
        tile_width = 16
        tile_height = 16
        tile_x = (tile_number % 9) * tile_width  # 9 is the number of columns
        tile_y = (tile_number // 9) * tile_height
            
            # Extract the specific tile
        self.image = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
        self.image.blit(tileset, (0, 0), (tile_x, tile_y, tile_width, tile_height))

        self.image = pygame.transform.scale(self.image, (30, 30))

        if not self.image:  # Si l'image n'a pas été chargée correctement
            print("Failed to load star image.")

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.launch_x = self.rect.x

    def update(self):
        self.rect.x += self.speed  # Débogage
        if self.rect.x > self.launch_x + 200: # Si l'étoile sort de l'écran, elle est supprimée
            print("Star removed.")
            self.kill()
