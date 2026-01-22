import pygame
import random

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
GROUND_HEIGHT = 250
CLOUD_HEIGHT = 75
PLAYER_WIDTH = 70
PLAYER_HEIGHT = 50
CLOUD_SPEED = 2
PLAYER_GRAVITY = 0.6
PLAYER_JUMP_VELOCITY = -12
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 50
OBSTACLE_SPEED = 5
MIN_OBSTACLE_DISTANCE = 250

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur Game")

# Load images
dino_sheet = pygame.image.load("sprites\dino.png").convert_alpha()
# Extract all frames from sprite sheet (3 frames horizontally)
frame_width = dino_sheet.get_width() // 3
frame_height = dino_sheet.get_height()
player_frames = []
for i in range(3):
    frame = dino_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
    frame = pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT))
    frame.set_colorkey((255, 255, 255))
    player_frames.append(frame)
# Create ducking image (wider and shorter)
player_duck_image = pygame.transform.scale(dino_sheet.subsurface((0, 0, frame_width, frame_height)), (80, 30))
player_duck_image.set_colorkey((255, 255, 255))
# Load cactus images
cacti_big_sheet = pygame.image.load("sprites\cacti-big.png").convert_alpha()
cacti_big_frame_width = cacti_big_sheet.get_width() // 6
cacti_big_image = cacti_big_sheet.subsurface((0, 0, cacti_big_frame_width, cacti_big_sheet.get_height()))
cacti_big_image = pygame.transform.scale(cacti_big_image, (25, 40))
cacti_big_image.set_colorkey((255, 255, 255))

cacti_small_sheet = pygame.image.load("sprites\cacti-small.png").convert_alpha()
cacti_small_frame_width = cacti_small_sheet.get_width() // 6
cacti_small_image = cacti_small_sheet.subsurface((0, 0, cacti_small_frame_width, cacti_small_sheet.get_height()))
cacti_small_image = pygame.transform.scale(cacti_small_image, (20, 30))
cacti_small_image.set_colorkey((255, 255, 255))

obstacle_images = [cacti_big_image, cacti_small_image]

# Load bird (pterodactyl) images
ptera_sheet = pygame.image.load("sprites\ptera.png").convert_alpha()
ptera_frame_width = ptera_sheet.get_width() // 2
ptera_frame_height = ptera_sheet.get_height()
ptera_frames = []
for i in range(2):
    frame = ptera_sheet.subsurface((i * ptera_frame_width, 0, ptera_frame_width, ptera_frame_height))
    frame = pygame.transform.scale(frame, (40, 30))
    frame.set_colorkey((255, 255, 255))
    ptera_frames.append(frame)

cloud_image = pygame.Surface((50, 20))
cloud_image.fill((255, 255, 255))

# Load ground image
ground_image = pygame.image.load("sprites\ground.png").convert_alpha()
ground_image = pygame.transform.scale(ground_image, (SCREEN_WIDTH, 100))
ground_image.set_colorkey((255, 255, 255))
ground_x = 0

# Load replay button
replay_button = pygame.image.load("sprites\\replay_button.png").convert_alpha()
replay_button.set_colorkey((255, 255, 255))
replay_button_rect = replay_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Create dark overlay for game over
dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
dark_overlay.fill((0, 0, 0))
dark_overlay.set_alpha(128)

# Set up font for score display
font = pygame.font.Font(None, 36)

# Load high score from file
high_score = 0
try:
    with open("high_score.txt", "r") as f:
        high_score = int(f.read()) 
except:
    pass

def save_high_score():
    with open("high_score.txt", "w") as f:
        f.write(str(high_score))

# Define classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = player_frames
        self.frame_index = 0
        self.animation_timer = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (50, GROUND_HEIGHT)
        self.velocity = 0
        self.is_ducking = False
        self._update_hitbox()

    def _update_hitbox(self):
        # Shrink hitbox on left side to account for tail
        self.hitbox = self.rect.inflate(-20, -6)
        self.hitbox.left = self.rect.left + 15

    def update(self):
        self.velocity += PLAYER_GRAVITY
        self.rect.move_ip(0, self.velocity)
        if self.rect.bottom > GROUND_HEIGHT:
            self.rect.bottom = GROUND_HEIGHT
            self.velocity = 0
        self._update_hitbox()
        # Animate while on ground and not ducking
        if self.rect.bottom >= GROUND_HEIGHT and not self.is_ducking:
            self.animation_timer += 1
            if self.animation_timer >= 8:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % 3
                self.image = self.frames[self.frame_index]

    def jump(self):
        if self.rect.bottom >= GROUND_HEIGHT and not self.is_ducking:
            self.velocity = PLAYER_JUMP_VELOCITY

    def duck(self):
        if not self.is_ducking:
            self.is_ducking = True
            self.image = player_duck_image
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (50, GROUND_HEIGHT)
            self.velocity = 0
            self._update_hitbox()

    def stand(self):
        if self.is_ducking:
            self.is_ducking = False
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (50, GROUND_HEIGHT)
            self._update_hitbox()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(obstacle_images)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (SCREEN_WIDTH, GROUND_HEIGHT)
        # Shrink hitbox for more forgiving collision
        self.hitbox = self.rect.inflate(-8, -8)
    
    def update(self):
        self.rect.move_ip(-OBSTACLE_SPEED, 0)
        self.hitbox.center = self.rect.center
        if self.rect.right < 0:
            self.kill()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = ptera_frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        # Birds fly at two heights:
        # High: passes over standing dino, no action needed
        # Low: must jump over or duck under
        bird_height = random.choice([GROUND_HEIGHT - 45, GROUND_HEIGHT - 90])
        self.rect.bottomleft = (SCREEN_WIDTH, bird_height)
        self.animation_timer = 0
        # Shrink hitbox for more forgiving collision
        self.hitbox = self.rect.inflate(-10, -10)

    def update(self):
        self.rect.move_ip(-OBSTACLE_SPEED, 0)
        self.hitbox.center = self.rect.center
        if self.rect.right < 0:
            self.kill()
        # Animate wings
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % 2
            self.image = self.frames[self.frame_index]

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

def reset_game():
    global all_sprites, obstacle_sprites, cloud_sprites, player, score, ground_x, game_over, high_score
    # Update high score if current score is higher
    if score > high_score:
        high_score = score
        save_high_score()
    all_sprites = pygame.sprite.Group()
    obstacle_sprites = pygame.sprite.Group()
    cloud_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    score = 0
    ground_x = 0
    game_over = False

# Set up game loop
clock = pygame.time.Clock()
score = 0
game_over = False
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over and replay_button_rect.collidepoint(event.pos):
                reset_game()
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
                elif event.key == pygame.K_DOWN:
                    player.duck()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player.stand()
    
    if not game_over:
        # Check if we can spawn a new obstacle (ensure minimum distance)
        can_spawn = True
        for obs in obstacle_sprites:
            if obs.rect.right > SCREEN_WIDTH - MIN_OBSTACLE_DISTANCE:
                can_spawn = False
                break

        # Spawn obstacles and clouds
        if can_spawn and random.random() < 0.02:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacle_sprites.add(obstacle)
        elif can_spawn and random.random() < 0.01:
            bird = Bird()
            all_sprites.add(bird)
            obstacle_sprites.add(bird)
        if random.random() < 0.01:
            cloud = Cloud()
            all_sprites.add(cloud)
            cloud_sprites.add(cloud)

        # Update sprites
        all_sprites.update()

        # Check for collisions using hitboxes
        for obs in obstacle_sprites:
            if player.hitbox.colliderect(obs.hitbox):
                game_over = True
                break
    
    # Draw the screen
    screen.fill((135, 206,250))
    # Fill bottom with ground color
    pygame.draw.rect(screen, (194, 178, 47), (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
    # Draw scrolling ground
    if not game_over:
        ground_x -= OBSTACLE_SPEED
        if ground_x <= -SCREEN_WIDTH:
            ground_x = 0
    screen.blit(ground_image, (ground_x, GROUND_HEIGHT - 80))
    screen.blit(ground_image, (ground_x + SCREEN_WIDTH, GROUND_HEIGHT - 80))
    all_sprites.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (83, 83, 83))
    screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
    high_score_text = font.render(f"HI: {high_score}", True, (83, 83, 83))
    screen.blit(high_score_text, (SCREEN_WIDTH - 150, 40))

    # Draw game over overlay and replay button
    if game_over:
        # Update high score when game ends
        if score > high_score:
            high_score = score
            save_high_score()
        screen.blit(dark_overlay, (0, 0))
        screen.blit(replay_button, replay_button_rect)

    pygame.display.flip()

    # Update score
    if not game_over:
        score += 1
    
    # Wait for next frame
    clock.tick(60)

# Clean up Pygame
pygame.quit()