import pygame
import os

# Initialize pygame
pygame.init()

# Create directories if they don't exist
os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/sounds", exist_ok=True)

# Create placeholder images
def create_background():
    image = pygame.Surface((800, 600))
    # Create a gradient sky
    for y in range(600):
        color = (135 - y // 10, 206 - y // 10, 235)
        pygame.draw.line(image, color, (0, y), (800, y))
    
    # Draw some clouds
    for x in [100, 300, 500, 700]:
        pygame.draw.ellipse(image, (255, 255, 255), (x, 100, 80, 40))
        pygame.draw.ellipse(image, (255, 255, 255), (x - 20, 110, 60, 30))
        pygame.draw.ellipse(image, (255, 255, 255), (x + 20, 110, 60, 30))
    
    # Draw ground
    pygame.draw.rect(image, (100, 50, 0), (0, 550, 800, 50))
    pygame.draw.rect(image, (0, 150, 0), (0, 530, 800, 20))
    
    pygame.image.save(image, "assets/images/background.png")
    print("Created background.png")

def create_mario():
    image = pygame.Surface((50, 50), pygame.SRCALPHA)
    
    # Red hat
    pygame.draw.rect(image, (255, 0, 0), (0, 0, 50, 20))
    pygame.draw.rect(image, (255, 0, 0), (10, 20, 30, 10))
    
    # Face
    pygame.draw.rect(image, (255, 200, 150), (10, 30, 30, 20))
    
    # Eyes 
    pygame.draw.rect(image, (255, 255, 255), (15, 35, 8, 8))
    pygame.draw.rect(image, (255, 255, 255), (30, 35, 8, 8))
    pygame.draw.rect(image, (0, 0, 0), (18, 38, 4, 4))
    pygame.draw.rect(image, (0, 0, 0), (33, 38, 4, 4))
    
    # Mustache
    pygame.draw.rect(image, (0, 0, 0), (15, 45, 20, 5))
    
    pygame.image.save(image, "assets/images/mario.png")
    print("Created mario.png")

def create_coin():
    image = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(image, (255, 215, 0), (15, 15), 15)
    pygame.draw.circle(image, (255, 255, 0), (15, 15), 12)
    pygame.draw.circle(image, (255, 215, 0), (15, 15), 8)
    pygame.draw.rect(image, (255, 255, 0), (12, 5, 6, 20))
    
    pygame.image.save(image, "assets/images/coin.png")
    print("Created coin.png")

def create_enemy():
    image = pygame.Surface((50, 50), pygame.SRCALPHA)
    
    # Body
    pygame.draw.rect(image, (150, 75, 0), (0, 20, 50, 30))
    
    # Shell pattern
    pygame.draw.rect(image, (0, 150, 0), (10, 25, 10, 10))
    pygame.draw.rect(image, (0, 150, 0), (30, 25, 10, 10))
    pygame.draw.rect(image, (0, 150, 0), (20, 35, 10, 10))
    
    # Eyes
    pygame.draw.rect(image, (255, 255, 255), (8, 10, 10, 10))
    pygame.draw.rect(image, (255, 255, 255), (32, 10, 10, 10))
    pygame.draw.rect(image, (0, 0, 0), (11, 13, 5, 5))
    pygame.draw.rect(image, (0, 0, 0), (35, 13, 5, 5))
    
    pygame.image.save(image, "assets/images/enemy.png")
    print("Created enemy.png")

def create_flag():
    image = pygame.Surface((50, 80), pygame.SRCALPHA)
    
    # Pole
    pygame.draw.rect(image, (150, 150, 150), (0, 0, 10, 80))
    
    # Flag
    pygame.draw.polygon(image, (0, 255, 0), [(10, 5), (45, 20), (10, 35)])
    
    pygame.image.save(image, "assets/images/flag.png")
    print("Created flag.png")

# Create all placeholder images
create_background()
create_mario()
create_coin() 
create_enemy()
create_flag()

print("All placeholder images created successfully!") 