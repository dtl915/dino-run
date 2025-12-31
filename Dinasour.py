import pygame
import random

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
GROUND_HEIGHT = 250
CLOUD_HEIGHT = 75
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
CLOUD_SPEED = 2
PLAYER_GRAVITY = 0.5
PLAYER_JUMP_VELOCITY = -10
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 50
OBSTACLE_SPEED = 5

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur Game")

# Load images
player_image = pygame.image.load("dino.png").convert_alpha()
player_image=pygame.transform.scale(player_image,(50,75))
obstacle_image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
obstacle_image.fill((255, 0, 0))
cloud_image = pygame.Surface((50, 20))
cloud_image.fill((255, 255, 255))

# Define classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (50, GROUND_HEIGHT)
        self.velocity = 0
    
    def update(self):
        self.velocity += PLAYER_GRAVITY
        self.rect.move_ip(0, self.velocity)
        if self.rect.bottom > GROUND_HEIGHT:
            self.rect.bottom = GROUND_HEIGHT
            self.velocity = 0
    
    def jump(self):
        self.velocity = PLAYER_JUMP_VELOCITY

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (SCREEN_WIDTH, GROUND_HEIGHT)
    
    def update(self):
        self.rect.move_ip(-OBSTACLE_SPEED, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cloud_image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 200), CLOUD_HEIGHT)
    
    def update(self):
        self.rect.move_ip(-CLOUD_SPEED, 0)
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

# Create sprite groups
all_sprites = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
cloud_sprites = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Set up game loop
clock = pygame.time.Clock()
score = 0
done = False

while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
    
    # Spawn obstacles and clouds
    if random.random() < 0.02:
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacle_sprites.add(obstacle)
    if random.random() < 0.01:
        cloud = Cloud()
        all_sprites.add(cloud)
        cloud_sprites.add(cloud)
    
    # Update sprites
    all_sprites.update()
    
    # Check for collisions
    if pygame.sprite.spritecollide(player, obstacle_sprites, False):
        done = True
    
    # Draw the screen
    screen.fill((135, 206,250))
    pygame.draw.rect(screen, (255, 255, 255), (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
    all_sprites.draw(screen)
    pygame.display.flip()
    
    # Update score
    score += 1
    
    # Wait for next frame
    clock.tick(60)

# Clean up Pygame
pygame.quit()