import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load and scale the player image
        try:
            self.image = pygame.image.load("assets/kirby.webp").convert_alpha()
            # Scale the image to desired size (30x30 in this case)
            self.image = pygame.transform.scale(self.image, (30, 30))
        except pygame.error as e:
            print(f"Couldn't load player image: {e}")
            # Fallback to colored rectangle if image loading fails
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 20, 147))  # Deep pink color
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)  # Use topleft instead of setting x,y separately
        
        # Movement attributes
        self.velocity_y = 0
        self.gravity = 0.4
        self.jump_speed = -5
        self.speed = 1

    def update(self):
        # Apply gravity
        self.velocity_y += self.gravity

        # Get keyboard input for horizontal movement only
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            self.jump()

    def jump(self):
        # Only allow jumping if we're not falling
        if self.velocity_y == 0:
            self.velocity_y = self.jump_speed 