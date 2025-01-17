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
        self.screen.fill((242, 216, 219))
        
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
        self.enemies_group = pygame.sprite.Group()  # Un groupe pour tous les ennemis

        # Updated enemy creation
        # Crée des ennemis et les ajoute au groupe
        for name, positions in self.spawn_points.items():
            for pos in positions:
                if name == 'guy':
                    guy = Guy(pos[0], pos[1])
                    self.guys.append(guy)
                    self.enemies_group.add(guy)  # Ajoute l'ennemi au groupe
                    print(f"Created guy at: ({pos[0]}, {pos[1]})")
                elif name == 'bird':
                    bird = Bird(pos[0], pos[1])
                    self.birds.append(bird)
                    self.enemies_group.add(bird)  # Ajoute l'ennemi au groupe
                    print(f"Created bird at: ({pos[0]}, {pos[1]})")
                elif name == 'flame':
                    flame = Flame(pos[0], pos[1])
                    self.flames.append(flame)
                    self.enemies_group.add(flame)  # Ajoute l'ennemi au groupe
                    print(f"Created flame at: ({pos[0]}, {pos[1]})")



    def handle_collision(self):
        # Gestion des collisions verticales
        next_y_position = self.player.rect.y + self.player.velocity_y
        self.player.rect.y = next_y_position

        # Vérifier les collisions avec les murs
        for wall in self.walls:
            if self.player.rect.colliderect(wall):
                # Annuler le mouvement vertical et gérer les sauts
                self.player.rect.y -= self.player.velocity_y
                if self.player.velocity_y > 0:  # Si le joueur tombe
                    self.player.can_jump = True
                self.player.velocity_y = 0
                break

        # Vérifier les collisions avec les ennemis
        in_collision = False
        for star in self.player.stars:    
            for enemy in self.enemies_group.sprites():
                if star.rect.colliderect(enemy.rect):  # Si l'étoile entre en collision avec un ennemi
                    enemy.kill()  # Supprime l'ennemi du groupe
                    star.kill()  # Supprime l'étoile du groupe
                    print(f"Ennemi {enemy} tué par une étoile !")
                    break 
        
        for enemy in self.enemies_group:
                if self.player.rect.colliderect(enemy.rect):
                    in_collision = True  # Collision détectée
                    if not self.player.invincible:  # Si pas déjà invincible
                        self.player.health -= 1
                        print(f"Collision avec un ennemi ! Santé restante : {self.player.health}")
                        self.player.invincible = True  # Activer l'invincibilité
                    break  # On sort après avoir traité une collision
        # Si aucune collision n'est détectée, désactiver l'invincibilité
        if not in_collision:
            self.player.invincible = False

        # Gestion des étoiles (collisions avec les ennemis)

        keys = pygame.key.get_pressed()

        # Déplacement à droite
        if keys[pygame.K_RIGHT]:
            self.player.rect.x += self.player.speed  # Déplace le joueur vers la droite
            
            # Vérifie la bordure droite
            if self.player.rect.right > self.SCREEN_WIDTH:  # Si le joueur dépasse la bordure droite
                self.player.rect.right = self.SCREEN_WIDTH  # Garde le joueur à l'intérieur de l'écran
            
            # Vérifie les collisions avec les murs
            for wall in self.walls:
                if self.player.rect.colliderect(wall):
                    self.player.rect.x -= self.player.speed  # Annule le déplacement si collision
                    break

        # Déplacement à gauche
        elif keys[pygame.K_LEFT]:
            self.player.rect.x -= self.player.speed  # Déplace le joueur vers la gauche
            
            # Vérifie la bordure gauche
            if self.player.rect.left < 0:  # Si le joueur dépasse la bordure gauche
                self.player.rect.left = 0  # Garde le joueur à l'intérieur de l'écran
            
            # Vérifie les collisions avec les murs
            for wall in self.walls:
                if self.player.rect.colliderect(wall):
                    self.player.rect.x += self.player.speed  # Annule le déplacement si collision
                    break



    def run(self):
        font = pygame.font.Font(None, 36) 
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.screen.fill(self.background_color)
            self.group.draw(self.screen)
            self.player.draw(self.screen)
            self.player.update()
            self.handle_collision()

            if self.player.health <= 0 or (self.player.rect.top > self.SCREEN_HEIGHT):  # Le joueur est tombé
                self.gameover()  # Appeler l'écran de Game Over

            self.enemies_group.update()  # Mets à jour tous les ennemis
            self.enemies_group.draw(self.screen)  # Dessine tous les ennemis
            # Dessiner chaque ennemi mis à jour

            health_text = font.render(f"Health: {self.player.health}", True, (255, 0, 0))
            self.screen.blit(health_text, (10, 10))
            
            pygame.display.flip()
            self.clock.tick(60)

    def gameover(self):
        """Affiche l'écran de Game Over avec les options."""
        # Couleur de fond noire
        self.screen.fill((242, 216, 219))

        # Police pour les messages
        font = pygame.font.Font(None, 74)  # Taille de la police : 74
        small_font = pygame.font.Font(None, 40)

        # Texte principal
        text = font.render("GAME OVER", True, (255, 255, 255))  # Blanc
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 3))
        self.screen.blit(text, text_rect)

        # Options
        restart_text = small_font.render("Press R to Restart", True, (255, 255, 255))
        quit_text = small_font.render("Press Q to Quit", True, (255, 255, 255))

        restart_rect = restart_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))

        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)

        # Mettre à jour l'écran
        pygame.display.flip()

        # Boucle d'attente pour les choix
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Gestion des touches
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:  # Recommencer
                    from menu import main  # Importer ici pour éviter le problème circulaire
                    main()
                    return
                elif keys[pygame.K_q]:  # Quitter
                    pygame.quit()
                    exit()
