import pygame
import random
import os
import math
from settings import *
from player import Player
from game_elements import Platform, Coin, Enemy, Flag, Powerup

class Level:
    def __init__(self, level_num, screen, jump_sound, coin_sound, powerup_sound, damage_sound):
        self.level_num = level_num
        self.screen = screen
        
        # Sound effects
        self.jump_sound = jump_sound
        self.coin_sound = coin_sound
        self.powerup_sound = powerup_sound
        self.damage_sound = damage_sound
        
        # Load the background
        try:
            self.background = pygame.image.load(os.path.join("assets", "images", "background.png"))
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except:
            # If background loading fails, create a placeholder
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill(SKY_BLUE)
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.flags = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        # Create the player
        self.player = Player(100, HEIGHT - 100, jump_sound)
        self.all_sprites.add(self.player)
        
        # Create the level
        self.create_level()
        
        # Track level completion status
        self.required_coins = int(self.total_coins * REQUIRED_COINS_PERCENT / 100)
        self.level_complete = False
        
        # Points earned this frame
        self.points_earned = 0
        self.powerup_obtained = False
    
    def create_level(self):
        # Determine the number of platforms, enemies, and coins based on level
        if self.level_num == 1:
            num_enemies = LEVEL_1_ENEMIES
            num_coins = LEVEL_1_COINS
        elif self.level_num == 2:
            num_enemies = LEVEL_2_ENEMIES
            num_coins = LEVEL_2_COINS
        else:
            num_enemies = LEVEL_3_ENEMIES
            num_coins = LEVEL_3_COINS
        
        # First platform (starting platform)
        start_platform_width = 250  # Increased width
        start_platform = Platform(0, HEIGHT - 40, start_platform_width, PLATFORM_HEIGHT)
        self.platforms.add(start_platform)
        self.all_sprites.add(start_platform)
        
        # Last platform (finish platform) - positioned further to extend map length
        finish_platform_width = 250  # Increased width
        finish_platform_x = WIDTH * 1.5 - finish_platform_width  # Extended distance by 1.5x
        finish_platform = Platform(finish_platform_x, HEIGHT - 40, finish_platform_width, PLATFORM_HEIGHT)
        self.platforms.add(finish_platform)
        self.all_sprites.add(finish_platform)
        
        # Add the flag
        flag = Flag(finish_platform_x + 130, HEIGHT - 40)
        self.flags.add(flag)
        self.all_sprites.add(flag)
        
        # Set the width of middle platforms - increase platform size
        platform_width = 180  # Increased size of middle platforms
        
        # Number of platforms based on level
        num_steps = 3  # Default value
        if self.level_num == 1:
            num_steps = LEVEL_1_PLATFORMS
        elif self.level_num == 2:
            num_steps = LEVEL_2_PLATFORMS
        else:
            num_steps = LEVEL_3_PLATFORMS
        
        # Space between start and finish (with extended map)
        available_space = (finish_platform_x - start_platform_width - 100)
        platforms_created = []
        first_platform = None  # Store first platform to ensure no enemies are placed on it
        
        # Create a stepped path of platforms where each platform helps reach the next
        prev_platform_end = start_platform_width  # End of previous platform
        
        for i in range(num_steps):
            # Calculate horizontal position of current platform - reduce distance from start to first platform
            if i == 0:
                # First platform is very close to the start
                start_offset = 80  # Reduced distance from 150 to 80
            else:
                # Other platforms are distributed evenly in remaining space
                start_offset = 80 + ((available_space - 80) * i) / (num_steps)
                
            x_position = start_platform_width + start_offset
            
            # Ensure no platforms are above or near the flag platform
            if x_position >= finish_platform_x - platform_width * 1.5:
                continue
                
            # Determine height in a gradual pattern to reach the goal
            # Each platform should be at a suitable height to reach the next one
            if i % 2 == 0:
                height_position = HEIGHT - 150 - (i * 70)
            else:
                height_position = HEIGHT - 180 - ((i-1) * 70)
            
            # Make sure the height is within allowed limits
            height_position = max(HEIGHT // 4, min(HEIGHT - 100, height_position))
            
            # Create the platform
            platform = Platform(x_position, height_position, platform_width, PLATFORM_HEIGHT)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
            platforms_created.append(platform)
            
            # Store the first platform
            if i == 0:
                first_platform = platform
            
            # Update the end of current platform to calculate distance to next platform
            prev_platform_end = x_position + platform_width
        
        # Create coins above platforms with increased spacing
        self.total_coins = num_coins
        coin_count = 0
        
        # Get the middle platforms
        middle_platforms = platforms_created.copy()
        
        # Distribute coins with greater spacing
        if len(middle_platforms) > 0 and num_coins > 0:
            # Choose platforms in random order
            random.shuffle(middle_platforms)
            
            # Distribute coins on selected platforms
            for platform in middle_platforms:
                if coin_count >= num_coins:
                    break
                
                # Place one coin above each selected platform at an appropriate distance
                x = platform.rect.centerx
                y = platform.rect.top - COIN_SIZE - 25
                
                coin = Coin(x, y, self.coin_sound)
                self.coins.add(coin)
                self.all_sprites.add(coin)
                coin_count += 1
        
        # Distribute any remaining coins
        remaining_coins = num_coins - coin_count
        if remaining_coins > 0 and len(middle_platforms) > 0:
            # Choose random platforms for remaining coins
            for _ in range(remaining_coins):
                platform = random.choice(middle_platforms)
                # Place the coin at a different position than the center of the platform
                offset = random.choice([-platform.rect.width//3, platform.rect.width//3])
                x = platform.rect.centerx + offset
                y = platform.rect.top - COIN_SIZE - 25
                
                coin = Coin(x, y, self.coin_sound)
                self.coins.add(coin)
                self.all_sprites.add(coin)
                coin_count += 1
        
        # Create enemies on middle platforms
        enemy_count = 0
        enemy_platforms = middle_platforms.copy()
        
        # Remove the first platform from the list of enemy platforms
        if first_platform in enemy_platforms:
            enemy_platforms.remove(first_platform)
        
        # Shuffle platforms to distribute enemies randomly
        random.shuffle(enemy_platforms)
        
        # Place enemies on platforms
        for platform in enemy_platforms:
            if enemy_count >= num_enemies:
                break
            
            x = platform.rect.centerx
            y = platform.rect.top
            enemy = Enemy(x, y, platform, self.level_num)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            enemy_count += 1
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Reset player velocity
        self.player.stop()
        
        # Handle player movement
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if keys[pygame.K_SPACE]:
            self.player.jump()
    
    def handle_powerup_collision(self):
        # Check if player collects a powerup
        for powerup in self.powerups:
            if self.player.rect.colliderect(powerup.rect):
                powerup.kill()
                self.powerup_sound.play()
                self.powerup_obtained = True
                self.points_earned += POWERUP_POINTS
    
    def update(self, has_powerup):
        # Reset points and powerup state
        self.points_earned = 0
        self.powerup_obtained = False
        
        # Handle player input
        self.handle_input()
        
        # Update all sprite groups separately to avoid parameter issues
        self.coins.update()
        self.enemies.update()
        self.flags.update() if hasattr(Flag, 'update') else None
        self.powerups.update()
        
        # Special update for player
        self.player.update(self.platforms, self.coins, self.enemies, WIDTH * 1.5, HEIGHT, has_powerup)
        
        # Handle powerup collisions
        self.handle_powerup_collision()
        
        # Check for coins and update coins collected text
        collected = self.player.coins_collected
        required = self.required_coins
        
        # Add points for any coins collected
        self.points_earned += self.player.last_collected * COIN_POINTS
        self.player.last_collected = 0  # Reset last collected
        
        # Check for win condition (reach the flag with enough coins)
        for flag in self.flags:
            if self.player.rect.colliderect(flag.rect):
                if collected >= required:
                    # Add points for reaching the flag
                    self.points_earned += FLAG_POINTS
                    return "win", self.points_earned, self.powerup_obtained
        
        # Check for lose condition
        if not self.player.alive:
            # Play damage sound
            self.damage_sound.play()
            return "lose", self.points_earned, self.powerup_obtained
        
        # Continue playing
        self.draw()
        return "playing", self.points_earned, self.powerup_obtained
    
    def draw(self):
        # Draw the background
        self.screen.blit(self.background, (0, 0))
        
        # Calculate camera offset (horizontal scrolling)
        offset_x = 0
        if self.player.rect.x > WIDTH / 2:
            offset_x = min(self.player.rect.x - WIDTH / 2, WIDTH * 0.5)
        
        # Draw all sprites with camera offset
        for sprite in self.all_sprites:
            pos = sprite.rect.copy()
            pos.x -= offset_x
            self.screen.blit(sprite.image, pos)
        
        # Draw the UI
        font = pygame.font.Font(None, 36)
        
        # Show coins collected
        coins_text = font.render(f"Coins: {self.player.coins_collected}/{self.required_coins}", True, WHITE)
        self.screen.blit(coins_text, (10, 10))
        
        # Show current level
        level_text = font.render(f"Level: {self.level_num}", True, WHITE)
        self.screen.blit(level_text, (WIDTH - 150, 10)) 