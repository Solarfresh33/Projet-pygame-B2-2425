import pygame
import pytmx
import pyscroll
from player import Player
from enemy import Enemy, Guy, Bird, Flame

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

        print(f"Number of colliders loaded: {len(self.walls)}")  # This should now show more than 0

        # Load spawn points from TMX
        # Updated spawn point handling
        self.spawn_points = {}
        for obj in tmx_data.get_layer_by_name('spawnpoints'):
            spawn_x = obj.x * zoom
            spawn_y = obj.y * zoom
            name = obj.name

            if name not in self.spawn_points:
                self.spawn_points[name] = []
            self.spawn_points[name].append((spawn_x, spawn_y))

            print(f"Loaded spawn point '{name}' at: ({spawn_x}, {spawn_y})")


        # Use player spawn point if it exists
        if 'player' in self.spawn_points:
            player_pos = self.spawn_points['player'][0]
            self.player = Player(player_pos[0], player_pos[1])
        else:
            print("No player spawn point found, using default position")
            self.player = Player(100, 100)

        print(f"Player position: ({self.player.rect.x}, {self.player.rect.y})")  # Debug print

        # Initialize enemy lists
        self.guys = []
        self.birds = []
        self.flames = []

        # Create enemies at their spawn points
        # Updated enemy creation
        for name, positions in self.spawn_points.items():
            for pos in positions:
                if name == 'guy':
                    self.guys.append(Guy(pos[0], pos[1]))
                    print(f"Created guy at: ({pos[0]}, {pos[1]})")
                elif name == 'bird':
                    self.birds.append(Bird(pos[0], pos[1]))
                    print(f"Created bird at: ({pos[0]}, {pos[1]})")
                elif name == 'flame':
                    self.flames.append(Flame(pos[0], pos[1]))
                    print(f"Created flame at: ({pos[0]}, {pos[1]})")


    def handle_collision(self):
        # Check if we would collide after vertical movement
        next_y_position = self.player.rect.y + self.player.velocity_y
        self.player.rect.y = next_y_position
        
        # Check for collisions at new position
        for wall in self.walls:
            if self.player.rect.colliderect(wall):
                # If collision, move back and stop vertical movement
                self.player.rect.y -= self.player.velocity_y
                if self.player.velocity_y > 0:  # Was falling
                    self.player.can_jump = True  # Reset jump ability when landing
                self.player.velocity_y = 0
                break

        # Handle horizontal movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            # Check if moving right would cause collision
            self.player.rect.x += self.player.speed
            for wall in self.walls:
                if self.player.rect.colliderect(wall):
                    self.player.rect.x -= self.player.speed
                    break
        elif keys[pygame.K_LEFT]:
            # Check if moving left would cause collision
            self.player.rect.x -= self.player.speed
            for wall in self.walls:
                if self.player.rect.colliderect(wall):
                    self.player.rect.x += self.player.speed
                    break

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

            # Draw player directly
            self.screen.blit(self.player.image, self.player.rect)

            # Draw all enemies
            for guy in self.guys:
                self.screen.blit(guy.image, guy.rect)
            for bird in self.birds:
                self.screen.blit(bird.image, bird.rect)
            for flame in self.flames:
                self.screen.blit(flame.image, flame.rect)
            
            pygame.display.flip()
            self.clock.tick(60)