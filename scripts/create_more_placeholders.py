import pygame
import os

# Initialize pygame
pygame.init()

# Create directories if they don't exist
os.makedirs("assets/images", exist_ok=True)

# Create placeholder images for new game elements
def create_box():
    image = pygame.Surface((40, 40), pygame.SRCALPHA)
    
    # Draw a question box
    pygame.draw.rect(image, (139, 69, 19), (0, 0, 40, 40))  # Brown background
    pygame.draw.rect(image, (255, 215, 0), (2, 2, 36, 36), 3)  # Gold border
    
    # Draw a question mark
    font = pygame.font.Font(None, 32)
    text = font.render("?", True, (255, 255, 255))
    text_rect = text.get_rect(center=(20, 20))
    image.blit(text, text_rect)
    
    pygame.image.save(image, "assets/images/box.png")
    print("Created box.png")

def create_broken_box():
    image = pygame.Surface((40, 40), pygame.SRCALPHA)
    
    # Draw a broken box
    pygame.draw.rect(image, (100, 50, 0), (0, 0, 40, 40))  # Darker brown background
    
    # Draw cracks
    pygame.draw.line(image, (50, 25, 0), (0, 0), (40, 40), 3)
    pygame.draw.line(image, (50, 25, 0), (0, 40), (40, 0), 3)
    pygame.draw.line(image, (50, 25, 0), (20, 0), (20, 40), 2)
    pygame.draw.line(image, (50, 25, 0), (0, 20), (40, 20), 2)
    
    pygame.image.save(image, "assets/images/broken_box.png")
    print("Created broken_box.png")

def create_powerup():
    image = pygame.Surface((35, 35), pygame.SRCALPHA)
    
    # Draw a mushroom-like power-up
    # Cap (red with white spots)
    pygame.draw.rect(image, (255, 0, 0), (0, 0, 35, 20), 0, 5)  # Red cap
    pygame.draw.circle(image, (255, 255, 255), (8, 10), 4)  # White spot 1
    pygame.draw.circle(image, (255, 255, 255), (24, 8), 3)  # White spot 2
    pygame.draw.circle(image, (255, 255, 255), (18, 15), 3)  # White spot 3
    
    # Stem (white)
    pygame.draw.rect(image, (255, 255, 255), (10, 20, 15, 15))
    
    # Add some shading
    pygame.draw.line(image, (200, 0, 0), (0, 5), (35, 5), 1)  # Shading on cap
    pygame.draw.line(image, (200, 200, 200), (10, 25), (25, 25), 1)  # Shading on stem
    
    pygame.image.save(image, "assets/images/powerup.png")
    print("Created powerup.png")

def create_mario_big():
    image = pygame.Surface((50, 75), pygame.SRCALPHA)
    
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
    
    # Body
    pygame.draw.rect(image, (255, 0, 0), (10, 50, 30, 25))  # Red shirt
    pygame.draw.rect(image, (0, 0, 255), (10, 65, 30, 10))  # Blue overalls
    
    pygame.image.save(image, "assets/images/mario_big.png")
    print("Created mario_big.png")

# Create all new placeholder images
create_box()
create_broken_box()
create_powerup()
create_mario_big()

print("All additional placeholder images created successfully!") 