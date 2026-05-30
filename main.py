import pygame
import sys
import os
import json
import random
import time
from settings import *
from level import Level

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Game")

# Load assets
try:
    # Sound effects
    jump_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "jump.wav"))
    coin_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "coin.wav"))
    powerup_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "powerup.wav"))
    damage_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "damage.wav"))
    victory_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "victory.wav"))
    game_over_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "gameover.wav"))
except:
    # Create empty sound objects as fallbacks
    print("Unable to load sound files. Using silent placeholders.")
    jump_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "jump.wav") if os.path.exists(os.path.join("assets", "sounds", "jump.wav")) else "")
    coin_sound = pygame.mixer.Sound("")
    powerup_sound = pygame.mixer.Sound("")
    damage_sound = pygame.mixer.Sound("")
    victory_sound = pygame.mixer.Sound("")
    game_over_sound = pygame.mixer.Sound("")

# Try to load background music
try:
    pygame.mixer.music.load(os.path.join("assets", "sounds", "background_music.wav"))
    has_music = True
except:
    has_music = False
    print("Background music not found")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Game states
MAIN_MENU = 0
INSTRUCTIONS = 1
PLAYING = 2
GAME_OVER = 3
LEVEL_COMPLETE = 4
WIN = 5
PAUSE = 6

game_state = MAIN_MENU

# Font setup
title_font = pygame.font.Font(None, 74)
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Save file path
SAVE_FILE = "game_save.json"

# Default save data
save_data = {
    "max_level_unlocked": 1,
    "coins_collected": 0,
    "high_score": 0
}

# Current game data
current_level = 1
max_levels = 3
total_coins_collected = 0
score = 0
lives = 3
level_start_time = 0
current_time = 0
time_limit = 300  # 5 minutes per level
has_powerup = False

# Create level
level = None

# Load save data
def load_save_data():
    global save_data, total_coins_collected
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r') as f:
                save_data = json.load(f)
                total_coins_collected = save_data["coins_collected"]
                print(f"Loaded save data: {save_data}")
        else:
            save_game()  # Create default save
    except Exception as e:
        print(f"Error loading save data: {e}")
        save_game()  # Create default save if there's an issue

# Save game data
def save_game():
    global save_data, total_coins_collected, score
    save_data["coins_collected"] = total_coins_collected
    # Update high score if current score is higher
    if score > save_data["high_score"]:
        save_data["high_score"] = score
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(save_data, f)
            print(f"Game saved: {save_data}")
    except Exception as e:
        print(f"Error saving game: {e}")

# Reset game state for new game
def reset_game_state():
    global score, lives, current_level, has_powerup
    score = 0
    lives = 3
    current_level = 1
    has_powerup = False

# Load save at startup
load_save_data()

# Button class for menus
class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=LIGHT_BLUE, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)  # Border
        
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

# Create menu buttons
play_button = Button(WIDTH//2 - 150, HEIGHT//2 - 60, 300, 60, "Start Game")
instruction_button = Button(WIDTH//2 - 150, HEIGHT//2 + 20, 300, 60, "Instructions")
quit_button = Button(WIDTH//2 - 150, HEIGHT//2 + 100, 300, 60, "Exit")

# Level select buttons
level_buttons = []
back_button = Button(WIDTH//2 - 150, HEIGHT - 100, 300, 60, "Back")
menu_button = Button(WIDTH//2 - 150, HEIGHT - 100, 300, 60, "Main Menu")
retry_button = Button(WIDTH//2 - 150, HEIGHT//2 + 100, 300, 60, "Retry")

# Generate level buttons
def create_level_buttons():
    global level_buttons
    level_buttons = []
    button_width = 200
    button_height = 60
    buttons_per_row = 3
    start_x = WIDTH//2 - ((button_width + 20) * buttons_per_row)//2
    start_y = HEIGHT//3
    
    for i in range(1, max_levels + 1):
        row = (i - 1) // buttons_per_row
        col = (i - 1) % buttons_per_row
        x = start_x + col * (button_width + 20)
        y = start_y + row * (button_height + 20)
        
        # Determine if level is locked
        color = BLUE if i <= save_data["max_level_unlocked"] else GRAY
        level_buttons.append(Button(x, y, button_width, button_height, f"Level {i}", color=color))

# Create initial level buttons
create_level_buttons()

def show_main_menu():
    # Draw background
    screen.fill(BLACK)
    
    # Draw title
    title = title_font.render("Super Mario Game", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//6))
    
    # Draw buttons
    play_button.draw()
    instruction_button.draw()
    quit_button.draw()
    
    # Show high score
    score_text = small_font.render(f"High Score: {save_data['high_score']}", True, WHITE)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))
    
    # Show max level
    level_text = small_font.render(f"Max Level: {save_data['max_level_unlocked']}", True, WHITE)
    screen.blit(level_text, (20, 20))

def show_instructions():
    # Draw background
    screen.fill(BLACK)
    
    # Draw title
    title = title_font.render("Instructions", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    # Draw instructions
    instructions = [
        "Controls:",
        "- Arrow keys to move left and right",
        "- Spacebar to jump",
        "- P or Escape to pause",
        "- M to return to the main menu",
        "",
        "Objective:",
        "- Collect coins for points",
        "- Avoid or jump on enemies",
        "- Reach the flag at the end of each level",
        "- Complete all 3 levels to win!",
        "",
        "Power-ups:",
        "- Mushroom: Makes you bigger and gives an extra life"
    ]
    
    y_pos = 150
    for line in instructions:
        text = small_font.render(line, True, WHITE)
        screen.blit(text, (WIDTH//4, y_pos))
        y_pos += 30
    
    # Draw back button
    back_button.draw()

def show_game_over():
    screen.fill(BLACK)
    title = title_font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = small_font.render("Press R to Restart Game", True, WHITE)
    menu_text = small_font.render("Press M to Return to Menu", True, WHITE)
    
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//3 + 30))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 30))
    screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT//2 + 70))
    
    # Draw retry button
    retry_button.draw()

def show_level_complete():
    screen.fill(BLACK)
    title = title_font.render(f"Level {current_level} Complete!", True, GREEN)
    
    # Calculate time bonus - 10 points for every 50 seconds remaining
    elapsed_time = current_time - level_start_time
    remaining_time = max(0, time_limit - elapsed_time)
    time_bonus_points = 10  # Points per 50 seconds
    time_bonus = int((remaining_time // 50) * time_bonus_points)
    
    # Display scores
    score_text = font.render(f"Level Score: {score}", True, WHITE)
    time_text = font.render(f"Time Bonus: {time_bonus}", True, WHITE)
    total_text = font.render(f"Total Score: {score + time_bonus}", True, WHITE)
    
    # Update max level unlocked
    if current_level >= save_data["max_level_unlocked"] and current_level < max_levels:
        save_data["max_level_unlocked"] = current_level + 1
        save_game()
        create_level_buttons()  # Refresh level buttons
    
    if current_level < max_levels:
        next_text = small_font.render("Press ENTER for next level", True, WHITE)
        screen.blit(next_text, (WIDTH//2 - next_text.get_width()//2, HEIGHT//2 + 100))
    else:
        next_text = small_font.render("Press ENTER to continue", True, WHITE)
        screen.blit(next_text, (WIDTH//2 - next_text.get_width()//2, HEIGHT//2 + 100))
    
    menu_text = small_font.render("Press M to Return to Menu", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//6))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//3))
    screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, HEIGHT//3 + 40))
    screen.blit(total_text, (WIDTH//2 - total_text.get_width()//2, HEIGHT//3 + 80))
    screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT//2 + 140))

def show_win_screen():
    screen.fill(BLACK)
    title = title_font.render("Congratulations! You Win!", True, GREEN)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {save_data['high_score']}", True, WHITE)
    restart_text = small_font.render("Press R to Play Again", True, WHITE)
    menu_text = small_font.render("Press M to Return to Menu", True, WHITE)
    
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//3 + 30))
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//3 + 70))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 30))
    screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT//2 + 70))
    
    # Draw retry button
    retry_button.draw()

def show_pause_menu():
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Draw pause menu
    title = title_font.render("PAUSED", True, WHITE)
    resume_text = small_font.render("Press P to Resume", True, WHITE)
    menu_text = small_font.render("Press M to Return to Menu", True, WHITE)
    restart_text = small_font.render("Press R to Restart Level", True, WHITE)
    
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    screen.blit(resume_text, (WIDTH//2 - resume_text.get_width()//2, HEIGHT//2))
    screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT//2 + 40))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 80))

def draw_game_ui():
    # Draw UI background
    ui_height = 50
    ui_bg = pygame.Surface((WIDTH, ui_height))
    ui_bg.fill(BLACK)
    ui_bg.set_alpha(180)  # Semi-transparent
    screen.blit(ui_bg, (0, 0))
    
    # Draw score
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 15))
    
    # Draw lives
    lives_text = small_font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH//2 - lives_text.get_width()//2, 15))
    
    # Draw timer
    elapsed_time = current_time - level_start_time
    remaining_time = max(0, time_limit - elapsed_time)
    # Show time in seconds only, rounded to nearest integer
    seconds = int(round(remaining_time))
    time_text = small_font.render(f"Time: {seconds}", True, WHITE)
    screen.blit(time_text, (WIDTH - time_text.get_width() - 20, 15))
    
    # Indicate if player has power-up
    if has_powerup:
        powerup_text = small_font.render("POWERED UP", True, GOLD)
        screen.blit(powerup_text, (WIDTH//2 + 100, 15))

# Start level
def start_level(level_num):
    global current_level, level, level_start_time, current_time
    current_level = level_num
    level = Level(current_level, screen, jump_sound, coin_sound, powerup_sound, damage_sound)
    level_start_time = time.time()
    current_time = level_start_time
    
    # Start background music
    if has_music:
        pygame.mixer.music.play(-1)  # Loop infinitely

# Update score based on game events
def update_score(points):
    global score
    score += points

# Game loop
running = True
while running:
    # Get current time if playing
    if game_state == PLAYING:
        current_time = time.time()
    
    # Get mouse position and click
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save game before quitting
            save_game()
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_click = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == PLAYING:
                    game_state = PAUSE
                elif game_state == PAUSE:
                    game_state = PLAYING
            
            if event.key == pygame.K_p:
                if game_state == PAUSE:
                    game_state = PLAYING
                elif game_state == PLAYING:
                    game_state = PAUSE
            
            if event.key == pygame.K_m:
                if game_state in [PLAYING, GAME_OVER, LEVEL_COMPLETE, WIN, PAUSE, INSTRUCTIONS]:
                    # Save progress and return to menu
                    if game_state == PLAYING:
                        save_game()
                        if has_music:
                            pygame.mixer.music.stop()  # Stop music when returning to menu
                    game_state = MAIN_MENU
            
            if event.key == pygame.K_RETURN:
                if game_state == LEVEL_COMPLETE:
                    # Add time bonus to score
                    elapsed_time = current_time - level_start_time
                    remaining_time = max(0, time_limit - elapsed_time)
                    time_bonus_points = 10  # Points per 50 seconds
                    time_bonus = int((remaining_time // 50) * time_bonus_points)
                    update_score(time_bonus)
                    
                    current_level += 1
                    if current_level <= max_levels:
                        start_level(current_level)
                        game_state = PLAYING
                    else:
                        game_state = WIN
                        if has_music:
                            pygame.mixer.music.stop()
                        victory_sound.play()
            
            if event.key == pygame.K_r:
                if game_state == GAME_OVER:
                    # Reset game completely
                    reset_game_state()
                    start_level(1)
                    game_state = PLAYING
                elif game_state == WIN:
                    # Reset game completely
                    reset_game_state()
                    start_level(1)
                    game_state = PLAYING
                elif game_state == PAUSE:
                    # Restart current level only
                    start_level(current_level)
                    game_state = PLAYING
    
    # Main menu logic
    if game_state == MAIN_MENU:
        # Update button hover states
        play_button.check_hover(mouse_pos)
        instruction_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        
        # Handle button clicks
        if play_button.is_clicked(mouse_pos, mouse_click):
            # Start a new game from level 1
            reset_game_state()
            start_level(1)
            game_state = PLAYING
        
        if instruction_button.is_clicked(mouse_pos, mouse_click):
            game_state = INSTRUCTIONS
        
        if quit_button.is_clicked(mouse_pos, mouse_click):
            # Save game before quitting
            save_game()
            running = False
        
        # Draw the main menu
        show_main_menu()
    
    # Instructions screen
    elif game_state == INSTRUCTIONS:
        # Update button hover states
        back_button.check_hover(mouse_pos)
        
        # Handle button clicks
        if back_button.is_clicked(mouse_pos, mouse_click):
            game_state = MAIN_MENU
        
        # Draw the instructions screen
        show_instructions()
    
    # Playing state
    elif game_state == PLAYING:
        # Check for time limit
        if current_time - level_start_time > time_limit:
            # Time's up - lose a life
            lives -= 1
            if lives <= 0:
                game_state = GAME_OVER
                if has_music:
                    pygame.mixer.music.stop()
                game_over_sound.play()
            else:
                # Restart current level
                start_level(current_level)
        
        # Update the game
        result, points, powerup_obtained = level.update(has_powerup)
        
        # Update score with any points earned
        if points > 0:
            update_score(points)
        
        # Check if powerup was obtained
        if powerup_obtained:
            has_powerup = True
            # Powerup also gives an extra life
            lives += 1
        
        # Draw the game UI
        draw_game_ui()
        
        # Check for win/lose conditions
        if result == "win":
            game_state = LEVEL_COMPLETE
        elif result == "lose":
            lives -= 1
            if lives <= 0:
                game_state = GAME_OVER
                if has_music:
                    pygame.mixer.music.stop()
                game_over_sound.play()
            else:
                # Restart current level
                start_level(current_level)
    
    # Game over state
    elif game_state == GAME_OVER:
        # Update button hover states
        retry_button.check_hover(mouse_pos)
        
        # Handle button clicks
        if retry_button.is_clicked(mouse_pos, mouse_click):
            reset_game_state()
            start_level(1)
            game_state = PLAYING
        
        show_game_over()
    
    # Level complete state
    elif game_state == LEVEL_COMPLETE:
        show_level_complete()
    
    # Win state
    elif game_state == WIN:
        # Update button hover states
        retry_button.check_hover(mouse_pos)
        
        # Handle button clicks
        if retry_button.is_clicked(mouse_pos, mouse_click):
            reset_game_state()
            start_level(1)
            game_state = PLAYING
        
        show_win_screen()
    
    # Pause state
    elif game_state == PAUSE:
        show_pause_menu()

    # Update the display
    pygame.display.flip()
    
    # Control the frame rate
    clock.tick(FPS)

# Save game before quitting
save_game()

# Quit Pygame
pygame.quit()
sys.exit() 