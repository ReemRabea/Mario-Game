import pygame
import os
import random
import math
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        
        # Try to add some texture to the platform
        for i in range(20):
            pos_x = random.randint(0, width-5)
            pos_y = random.randint(0, height-5)
            size = random.randint(3, 8)
            color = (random.randint(100, 120), random.randint(50, 60), random.randint(10, 20))
            pygame.draw.circle(self.image, color, (pos_x, pos_y), size)
        
        # Add a border to the platform
        pygame.draw.rect(self.image, (100, 50, 0), (0, 0, width, height), 2)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, coin_sound=None):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join("assets", "images", "coin.png"))
            self.image = pygame.transform.scale(self.image, (COIN_SIZE, COIN_SIZE))
        except:
            # If image loading fails, create a placeholder
            self.image = pygame.Surface((COIN_SIZE, COIN_SIZE))
            self.image.fill((255, 215, 0))  # Gold color
            pygame.draw.circle(self.image, (255, 255, 0), (COIN_SIZE//2, COIN_SIZE//2), COIN_SIZE//2)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Animation variables
        self.animation_count = 0
        self.original_y = y
        
        # Sound
        self.coin_sound = coin_sound
    
    def update(self):
        # Make the coin bob up and down
        self.animation_count += 0.1
        self.rect.y = self.original_y + int(5 * math.sin(self.animation_count))
    
    def kill(self):
        # Play sound when collected
        if self.coin_sound:
            self.coin_sound.play()
        super().kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, platform, level_num):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join("assets", "images", "enemy.png"))
            self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
        except:
            # If image loading fails, create a placeholder
            self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
            self.image.fill((0, 0, 0))
            pygame.draw.rect(self.image, (255, 0, 0), (0, 0, ENEMY_WIDTH, ENEMY_HEIGHT//2))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - ENEMY_HEIGHT
        
        # Movement variables
        self.platform = platform
        self.direction = 1  # 1 for right, -1 for left
        self.speed = ENEMY_SPEED + (level_num - 1)  # Speed increases with level
    
    def update(self):
        # Move the enemy
        self.rect.x += self.direction * self.speed
        
        # Check if the enemy is at the edge of its platform
        if self.rect.right > self.platform.rect.right - 10:
            self.rect.right = self.platform.rect.right - 10
            self.direction *= -1
        elif self.rect.left < self.platform.rect.left + 10:
            self.rect.left = self.platform.rect.left + 10
            self.direction *= -1

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join("assets", "images", "flag.png"))
            self.image = pygame.transform.scale(self.image, (50, 80))
        except:
            # If image loading fails, create a placeholder
            self.image = pygame.Surface((50, 80))
            self.image.fill((255, 255, 255))
            # Draw a flag pole
            pygame.draw.rect(self.image, (150, 150, 150), (0, 0, 10, 80))
            # Draw a flag
            pygame.draw.polygon(self.image, (0, 255, 0), [(10, 5), (10, 35), (45, 20)])
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 80  # Position the flag slightly above the platform

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join("assets", "images", "powerup.png"))
            self.image = pygame.transform.scale(self.image, (POWERUP_SIZE, POWERUP_SIZE))
        except:
            # If image loading fails, create a placeholder
            self.image = pygame.Surface((POWERUP_SIZE, POWERUP_SIZE))
            self.image.fill(RED)
            # Draw a mushroom-like shape
            pygame.draw.circle(self.image, RED, (POWERUP_SIZE//2, POWERUP_SIZE//2), POWERUP_SIZE//2)
            pygame.draw.rect(self.image, WHITE, (POWERUP_SIZE//4, POWERUP_SIZE//4, POWERUP_SIZE//2, POWERUP_SIZE//4))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement variables
        self.velocity_x = random.choice([-1, 1])  # Move left or right randomly
        self.velocity_y = 0
        
        # Animation variables
        self.animation_count = 0
    
    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY * 0.5  # Lighter gravity for powerups
        
        # Move powerup
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Bounce off screen edges
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.velocity_x *= -1
        
        # Don't fall off bottom of screen
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = -5  # Bounce up
        
        # Make powerup pulse
        self.animation_count += 0.1
        scale = 1.0 + 0.1 * math.sin(self.animation_count)
        center = self.rect.center
        self.rect.width = int(POWERUP_SIZE * scale)
        self.rect.height = int(POWERUP_SIZE * scale)
        self.rect.center = center 