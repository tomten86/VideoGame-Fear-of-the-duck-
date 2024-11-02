import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fear of the Duck")

# Load the background image (if you have one)
# If you prefer a solid color background, you can fill the window with a color
# For a light blue background without an image, you can use:
# window.fill((173, 216, 230))  # Light blue color

# Font for text
font = pygame.font.SysFont(None, 36)

# Class for the player (child)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the child's image
        self.image_original = pygame.image.load("child.png").convert_alpha()
        # Scale the image to fit the game
        self.image = pygame.transform.scale(self.image_original, (50, 50))
        self.rect = self.image.get_rect()
        # Start position of the player
        self.rect.center = (WIDTH // 2, HEIGHT - 75)
        self.speed = 5
        self.lives = 3

    def update(self, keys_pressed):
        # Movement controls
        if keys_pressed[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

# Class for the duck
class Duck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the duck's image
        self.image_original = pygame.image.load("duck.png").convert_alpha()
        # Scale the image to fit the game
        self.image = pygame.transform.scale(self.image_original, (50, 50))
        self.rect = self.image.get_rect()
        # Start position of the duck
        self.rect.center = (WIDTH // 2, 50)
        self.speed = 2

    def update(self, player_pos):
        # Simple movement towards the player
        if self.rect.x < player_pos[0]:
            self.rect.x += self.speed
        if self.rect.x > player_pos[0]:
            self.rect.x -= self.speed
        if self.rect.y < player_pos[1]:
            self.rect.y += self.speed
        if self.rect.y > player_pos[1]:
            self.rect.y -= self.speed

# Class for obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a gray rectangle as the obstacle
        self.image = pygame.Surface((random.randint(20, 100), 20))
        self.image.fill((128, 128, 128))  # Gray color
        self.rect = self.image.get_rect()
        # Random position for the obstacle
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(100, HEIGHT - 150)

# Sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

player = Player()
duck = Duck()
all_sprites.add(player)
all_sprites.add(duck)

# Create obstacles
for _ in range(5):
    obstacle = Obstacle()
    obstacles.add(obstacle)
    all_sprites.add(obstacle)

# Clock to control frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    clock.tick(60)  # Limit to 60 frames per second

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # Update sprites
    keys_pressed = pygame.key.get_pressed()
    player.update(keys_pressed)
    duck.update(player.rect.center)

    # Collision detection
    if pygame.sprite.collide_rect(player, duck):
        player.lives -= 1
        player.rect.center = (WIDTH // 2, HEIGHT - 75)  # Reset position
        if player.lives <= 0:
            running = False  # Game over

    if pygame.sprite.spritecollide(player, obstacles, False):
        # If the player hits an obstacle, reduce speed
        player.speed = 2
    else:
        player.speed = 5

    # Drawing
    window.fill((173, 216, 230))  # Light blue background
    all_sprites.draw(window)

    # Display lives
    lives_text = font.render(f"Lives: {player.lives}", True, (0, 0, 0))
    window.blit(lives_text, (10, 10))

    pygame.display.flip()

# End of the game
pygame.quit()
print("Game Over")
