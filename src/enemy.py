import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_number):
        super().__init__()
        try:
            # Load the tileset image
            tileset = pygame.image.load("levels/kirby-like.png").convert_alpha()
            
            # Calculate the position of the tile in the tileset
            tile_width = 16
            tile_height = 16
            tile_x = (tile_number % 9) * tile_width  # 9 is the number of columns
            tile_y = (tile_number // 9) * tile_height
            
            # Extract the specific tile
            self.image = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
            self.image.blit(tileset, (0, 0), (tile_x, tile_y, tile_width, tile_height))
            
            # Scale the image
            self.image = pygame.transform.scale(self.image, (30, 30))
            
        except pygame.error as e:
            print(f"Couldn't load enemy image: {e}")
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 0, 0))  # Red fallback color
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Guy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 19)  # Tile 19 for guy

class Bird(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 28)  # Tile 28 for bird

class Flame(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 37)  # Tile 37 for flame 