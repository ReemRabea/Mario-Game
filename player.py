import pygame
import os
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, jump_sound):
        super().__init__()
        # Load the player image
        try:
            self.small_image = pygame.image.load(os.path.join("assets", "images", "mario.png"))
            self.big_image = pygame.image.load(os.path.join("assets", "images", "mario_big.png"))
            self.small_image = pygame.transform.scale(self.small_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.big_image = pygame.transform.scale(self.big_image, (PLAYER_WIDTH, PLAYER_HEIGHT * 1.5))
            self.image = self.small_image
        except:
            # If image loading fails, create placeholders
            self.small_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.small_image.fill(RED)
            self.big_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT * 1.5))
            self.big_image.fill(RED)
            # Add some details
            pygame.draw.rect(self.small_image, BLUE, (0, 0, PLAYER_WIDTH, PLAYER_HEIGHT//3))  # Hat
            pygame.draw.rect(self.big_image, BLUE, (0, 0, PLAYER_WIDTH, PLAYER_HEIGHT//2))  # Hat
            self.image = self.small_image
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Player movement variables
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False
        self.on_ground = False
        self.jump_power = PLAYER_JUMP_POWER
        self.speed = PLAYER_SPEED
        
        # Facing direction (for sprite flipping)
        self.facing_right = True
        
        # Sound effects
        self.jump_sound = jump_sound
        
        # Game state tracking
        self.coins_collected = 0
        self.last_collected = 0  # Track coins collected since last save
        self.alive = True
        
        # Power-up state
        self.is_big = False
        self.invincible = False
        self.invincible_timer = 0
        
        # Animation variables
        self.animation_frame = 0
        self.animation_cooldown = 0
    
    def update(self, platforms, coins, enemies, screen_width, screen_height, has_powerup=False):
        # Update power-up state
        if has_powerup and not self.is_big:
            self.become_big()
        
        # Update invincibility
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        # Update animation
        self.animation_cooldown -= 1
        if self.animation_cooldown <= 0:
            self.animation_frame = (self.animation_frame + 1) % 4  # 4 animation frames
            self.animation_cooldown = 6  # Frames between animation updates
        
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Move the player
        self.rect.x += self.velocity_x
        
        # Handle platform collisions (horizontal)
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:  # Moving right
                    self.rect.right = platform.rect.left
                elif self.velocity_x < 0:  # Moving left
                    self.rect.left = platform.rect.right
        
        # Apply vertical movement
        self.rect.y += self.velocity_y
        
        # Handle platform collisions (vertical)
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.velocity_y = 0
                elif self.velocity_y < 0:  # Jumping
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
        
        # Check for coin collection
        for coin in coins:
            if self.rect.colliderect(coin.rect):
                coin.kill()
                self.coins_collected += 1
                self.last_collected += 1  # Track for saving progress
        
        # Check for enemy collisions
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect) and not self.invincible:
                # If jumping on top of enemy, kill the enemy
                if self.velocity_y > 0 and self.rect.bottom < enemy.rect.centery + 10:
                    enemy.kill()
                    self.velocity_y = -self.jump_power / 2  # Small bounce
                else:
                    # Player gets hit
                    if self.is_big:
                        # Lose power-up but don't die
                        self.become_small()
                        self.invincible = True
                        self.invincible_timer = 60  # 1 second invincibility after hit
                    else:
                        self.alive = False
        
        # Screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        
        # Check if player fell off the bottom of the screen
        if self.rect.top > screen_height:
            self.alive = False
        
        # Apply flipping based on direction
        if self.facing_right and self.velocity_x < 0:
            self.facing_right = False
            self.flip_image()
        elif not self.facing_right and self.velocity_x > 0:
            self.facing_right = True
            self.flip_image()
    
    def jump(self):
        if self.on_ground:
            self.velocity_y = -self.jump_power
            self.is_jumping = True
            self.on_ground = False
            self.jump_sound.play()
    
    def move_left(self):
        self.velocity_x = -self.speed
        self.facing_right = False
    
    def move_right(self):
        self.velocity_x = self.speed
        self.facing_right = True
    
    def stop(self):
        self.velocity_x = 0
    
    def reset(self, x, y):
        # Reset player position and state
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.coins_collected = 0
        self.last_collected = 0  # Reset last collected coins
        self.alive = True
        self.become_small()  # Reset to small state
        self.invincible = False
        self.invincible_timer = 0
    
    def become_big(self):
        if not self.is_big:
            self.is_big = True
            self.image = self.big_image
            # Adjust rect to maintain bottom position
            bottom = self.rect.bottom
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.x = self.rect.x  # Keep same x position
            # Enhance abilities
            self.jump_power = PLAYER_JUMP_POWER * 1.2
            self.speed = PLAYER_SPEED * 1.2
    
    def become_small(self):
        if self.is_big:
            self.is_big = False
            self.image = self.small_image
            # Adjust rect to maintain bottom position
            bottom = self.rect.bottom
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.x = self.rect.x  # Keep same x position
            # Reset abilities
            self.jump_power = PLAYER_JUMP_POWER
            self.speed = PLAYER_SPEED
    
    def flip_image(self):
        # Flip the image based on direction
        if self.is_big:
            self.big_image = pygame.transform.flip(self.big_image, True, False)
            self.image = self.big_image
        else:
            self.small_image = pygame.transform.flip(self.small_image, True, False)
            self.image = self.small_image 