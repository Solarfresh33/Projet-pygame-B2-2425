import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, animation_tiles):
        super().__init__()
        try:
            # Load the tileset image
            tileset = pygame.image.load("levels/kirby-like.png").convert_alpha()
            self.sprites = []  # Initialiser une liste pour les sprites d'animation
            self.last_update_time = pygame.time.get_ticks()  # Temps du dernier changement de sprite
            self.animation_delay = 400  # Délai entre les animations en millisecondes (1 seconde)
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

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.animation_delay:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]
            self.last_update_time = current_time



class Guy(Enemy):
    def __init__(self, x, y):
        animation_tiles = [18, 19]
        super().__init__(x, y, animation_tiles)  # Tile 19 for guy
        
        self.speed = 0.6  # Vitesse de déplacement
        self.direction = -1  # 1 pour aller à droite, -1 pour aller à gauche
        self.boundary_left = x - 120  # Limite gauche
        self.boundary_right = x + 110  # Limite droite
        self.facing_right = True  
    def update(self):
        # Animation
        

        # Mouvement horizontal
        self.rect.x += self.speed * self.direction

        # Inverser la direction si on atteint une limite
        if self.rect.left <= self.boundary_left or self.rect.right >= self.boundary_right:
            self.direction *= -1
            self.facing_right = not self.facing_right  # Inverser la direction visuelle
            # Retourner les sprites horizontalement
            self.sprites = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites]

        super().update()


class Bird(Enemy):
    def __init__(self, x, y):
        animation_tiles = [27, 28]
        super().__init__(x, y, animation_tiles)  # Tile 28 for bird
        self.speed = 1
        self.direction = -1  # 1 pour aller à droite, -1 pour aller à gauche
        self.boundary_left = x - 1000  # Limite gauche
        self.boundary_right = x + 200  # Limite droite
        self.facing_right = True  # True si l'oiseau regarde à droite

    def update(self):
        # Déplacement horizontal
        self.rect.x += self.speed * self.direction

        # Inverser la direction si on atteint une limite
        if self.rect.left <= self.boundary_left or self.rect.right >= self.boundary_right:
            self.direction *= -1
            self.facing_right = not self.facing_right  # Inverser la direction visuelle
            # Retourner les sprites horizontalement
            self.sprites = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites]

        # Mise à jour de l'animation (héritée de Enemy)
        super().update()



class Flame(Enemy):
    def __init__(self, x, y):
        animation_tiles = [36, 37]
        super().__init__(x, y, animation_tiles)  # Tile 37 for flame 