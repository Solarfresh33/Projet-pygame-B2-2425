import pygame
import pytmx
import pyscroll
from player import Player

class Game:

    def __init__(self):
        self.SCREEN_WIDTH = 945
        self.SCREEN_HEIGHT = 700
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Kirby Platformer")

        # Load TMX data
        tmx_data = pytmx.util_pygame.load_pygame('./levels/level-1.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)

        # Calculate zoom
        map_width = tmx_data.width * tmx_data.tilewidth
        map_height = tmx_data.height * tmx_data.tileheight
        scale_x = self.SCREEN_WIDTH / map_width
        scale_y = self.SCREEN_HEIGHT / map_height
        zoom = min(scale_x, scale_y)  # Keep proportions using smallest scale

        print(f"Zoom factor: {zoom}")  # Debug print

        # Create renderer with adjusted zoom
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = zoom  # Adjust scaling

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

        # Background color
        self.background_color = (242, 216, 219)

        # Clock for FPS limiting
        self.clock = pygame.time.Clock()

        # Load colliders from TMX
        self.walls = []
        for obj in tmx_data.get_layer_by_name('colliders'):  # Get colliders layer specifically
            rect = pygame.Rect(
                obj.x * zoom, 
                obj.y * zoom, 
                obj.width * zoom, 
                obj.height * zoom
            )
            self.walls.append(rect)

        print(f"Number of walls loaded: {len(self.walls)}")  # This should now show more than 0

        # Get player spawn point from TMX
        spawn_found = False
        for obj in tmx_data.objects:
            if obj.name == "player":  # Find the player spawn point
                # Convert spawn position to account for zoom
                spawn_x = obj.x * zoom
                spawn_y = obj.y * zoom
                print(f"Found player spawn point at: ({spawn_x}, {spawn_y})")  # Debug print
                self.player = Player(spawn_x, spawn_y)
                spawn_found = True
                break

        if not spawn_found:
            print("No spawn point found, using default position")  # Debug print
            self.player = Player(100, 100)  # Changed default position to be more visible

        print(f"Player position: ({self.player.rect.x}, {self.player.rect.y})")  # Debug print

    def handle_collision(self):
        # Handle vertical collisions
        self.player.rect.y += self.player.velocity_y
        for wall in self.walls:
            if self.player.rect.colliderect(wall):
                if self.player.velocity_y > 0:  # Falling
                    self.player.rect.bottom = wall.top
                    self.player.velocity_y = 0
                elif self.player.velocity_y < 0:  # Jumping
                    self.player.rect.top = wall.bottom
                    self.player.velocity_y = 0

        # Handle horizontal collisions
        self.player.rect.x += (pygame.key.get_pressed()[pygame.K_RIGHT] - pygame.key.get_pressed()[pygame.K_LEFT]) * self.player.speed
        for wall in self.walls:
            if self.player.rect.colliderect(wall):
                if pygame.key.get_pressed()[pygame.K_RIGHT]:  # Moving right
                    self.player.rect.right = wall.left
                elif pygame.key.get_pressed()[pygame.K_LEFT]:  # Moving left
                    self.player.rect.left = wall.right

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update player and handle collisions
            self.player.update()
            self.handle_collision()

            # Clear screen and draw
            self.screen.fill(self.background_color)
            
            # Draw the map and sprites
            self.group.draw(self.screen)

            # Draw player directly instead of through group
            self.screen.blit(self.player.image, self.player.rect)

           
            # Print positions every second
            if pygame.time.get_ticks() % 60 == 0:
                print(f"Player rect position: {self.player.rect.topleft}")
                print(f"Player sprite position: {self.player.rect.x}, {self.player.rect.y}")
            
            pygame.display.flip()
            self.clock.tick(60) 