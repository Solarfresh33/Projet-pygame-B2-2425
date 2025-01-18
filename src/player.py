import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load and scale the player image
        try:
            self.image = pygame.image.load("assets/kirby.png").convert_alpha()
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
        self.gravity = 0.7
        self.jump_speed = -15
        self.speed = 2
        self.health = 100
        self.can_jump = True  # Add this to control jump

        self.invincible = False  # Par défaut, pas invincible

    def update(self):
        

        self.velocity_y += self.gravity

        # Get keyboard input for jumping
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_jump:
            self.jump()

    def jump(self):
        self.velocity_y = self.jump_speed
        self.can_jump = False  # Prevent further jumps until landing 