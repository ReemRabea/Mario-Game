import pygame
import os
import numpy as np
from array import array
from math import sin, pi

def create_sound_directory():
    # Create directory if it doesn't exist
    os.makedirs("assets/sounds", exist_ok=True)

def create_jump_sound():
    # Create a simple rising tone
    sample_rate = 44100
    duration = 0.4  # seconds
    samples = int(duration * sample_rate)
    
    # Create buffer
    buf = array('h', [0] * samples)
    max_amplitude = 2**15 - 1  # maximum amplitude for int16
    
    # Generate rising tone
    for i in range(samples):
        t = float(i) / sample_rate  # time in seconds
        frequency = 300 + 1200 * t / duration  # from 300Hz to 1500Hz
        buf[i] = int(max_amplitude * 0.6 * sin(2 * pi * frequency * t) * (1 - t / duration))
    
    # Create sound from buffer
    sound = pygame.mixer.Sound(buffer=buf)
    pygame.mixer.Sound.save(sound, "assets/sounds/jump.wav")
    print("Created jump.wav")

def create_coin_sound():
    # Create a simple "ping" sound
    sample_rate = 44100
    duration = 0.2  # seconds
    samples = int(duration * sample_rate)
    
    # Create buffer
    buf = array('h', [0] * samples)
    max_amplitude = 2**15 - 1  # maximum amplitude for int16
    
    # Generate ping sound
    for i in range(samples):
        t = float(i) / sample_rate  # time in seconds
        frequency = 1200  # Higher pitch for coin
        buf[i] = int(max_amplitude * 0.5 * sin(2 * pi * frequency * t) * (1 - t / duration))
    
    # Create sound from buffer
    sound = pygame.mixer.Sound(buffer=buf)
    pygame.mixer.Sound.save(sound, "assets/sounds/coin.wav")
    print("Created coin.wav")

def create_powerup_sound():
    # Create a powerup sound
    sample_rate = 44100
    duration = 0.6  # seconds
    samples = int(duration * sample_rate)
    
    # Create buffer
    buf = array('h', [0] * samples)
    max_amplitude = 2**15 - 1  # maximum amplitude for int16
    
    # Generate powerup sound (ascending notes)
    for i in range(samples):
        t = float(i) / sample_rate  # time in seconds
        part = int(t / (duration / 3))  # which of 3 notes
        frequency = 400 * (1.5 ** part)  # Increase pitch for each part
        buf[i] = int(max_amplitude * 0.7 * sin(2 * pi * frequency * t))
    
    # Create sound from buffer
    sound = pygame.mixer.Sound(buffer=buf)
    pygame.mixer.Sound.save(sound, "assets/sounds/powerup.wav")
    print("Created powerup.wav")

def create_damage_sound():
    # Create a damage sound
    sample_rate = 44100
    duration = 0.3  # seconds
    samples = int(duration * sample_rate)
    
    # Create buffer
    buf = array('h', [0] * samples)
    max_amplitude = 2**15 - 1  # maximum amplitude for int16
    
    # Generate damage sound (descending notes with noise)
    for i in range(samples):
        t = float(i) / sample_rate  # time in seconds
        frequency = 300 - 150 * t / duration  # Decrease pitch
        noise = np.random.normal(0, 0.3)  # Add some noise
        buf[i] = int(max_amplitude * 0.6 * (sin(2 * pi * frequency * t) + noise) * (1 - t / duration))
    
    # Create sound from buffer
    sound = pygame.mixer.Sound(buffer=buf)
    pygame.mixer.Sound.save(sound, "assets/sounds/damage.wav")
    print("Created damage.wav")

def create_victory_sound():
    # Create a victory fanfare
    sample_rate = 44100
    duration = 1.0  # seconds
    samples = int(duration * sample_rate)
    
    # Create buffer
    buf = array('h', [0] * samples)
    max_amplitude = 2**15 - 1  # maximum amplitude for int16
    
    # Generate victory sound (fanfare sequence)
    notes = [440, 550, 660, 880]  # Frequencies for notes
    note_duration = duration / len(notes)
    
    for i in range(samples):
        t = float(i) / sample_rate  # time in seconds
        note_index = min(int(t / note_duration), len(notes) - 1)
        frequency = notes[note_index]
        buf[i] = int(max_amplitude * 0.7 * sin(2 * pi * frequency * t))
    
    # Create sound from buffer
    sound = pygame.mixer.Sound(buffer=buf)
    pygame.mixer.Sound.save(sound, "assets/sounds/victory.wav")
    print("Created victory.wav")

def create_game_over_sound():
    # Create a game over sound
    sample_rate = 44100
    duration = 1.0  # seconds
    samples = int(duration * sample_rate)
    
    # Create buffer
    buf = array('h', [0] * samples)
    max_amplitude = 2**15 - 1  # maximum amplitude for int16
    
    # Generate game over sound (descending notes)
    notes = [440, 349, 261, 220]  # Frequencies for notes
    note_duration = duration / len(notes)
    
    for i in range(samples):
        t = float(i) / sample_rate  # time in seconds
        note_index = min(int(t / note_duration), len(notes) - 1)
        frequency = notes[note_index]
        buf[i] = int(max_amplitude * 0.7 * sin(2 * pi * frequency * t))
    
    # Create sound from buffer
    sound = pygame.mixer.Sound(buffer=buf)
    pygame.mixer.Sound.save(sound, "assets/sounds/gameover.wav")
    print("Created gameover.wav")

def create_background_music():
    # Create a simple background music loop
    sample_rate = 44100
    duration = 8.0  # seconds
    samples = int(duration * sample_rate)
    
    # Create buffer
    buf = array('h', [0] * samples)
    max_amplitude = 2**15 - 1  # maximum amplitude for int16
    
    # Base melody notes and rhythm
    notes = [
        (392, 0.5), (392, 0.5), (0, 0.5), (392, 0.5),  # G G - G
        (0, 0.5), (329.63, 0.5), (392, 0.5), (0, 0.5),  # - E G -
        (261.63, 0.5), (0, 0.5), (0, 0.5), (220, 0.5),  # C - - A
        (0, 0.25), (246.94, 0.5), (0, 0.25), (261.63, 0.5), (0, 0.5)  # - B - C -
    ]
    
    # Generate simple music
    current_time = 0
    for freq, note_duration in notes:
        end_time = current_time + note_duration
        note_samples = int(note_duration * sample_rate)
        
        for i in range(note_samples):
            if current_time + float(i) / sample_rate < end_time:
                sample_index = int(current_time * sample_rate) + i
                if sample_index < samples:
                    if freq > 0:  # Skip silent notes (freq = 0)
                        t = float(i) / sample_rate
                        buf[sample_index] = int(max_amplitude * 0.5 * sin(2 * pi * freq * t))
        
        current_time = end_time
    
    # Create sound from buffer
    sound = pygame.mixer.Sound(buffer=buf)
    pygame.mixer.Sound.save(sound, "assets/sounds/background_music.wav")
    print("Created background_music.wav")

if __name__ == "__main__":
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Create sounds directory
    create_sound_directory()
    
    # Create all sound effects
    create_jump_sound()
    create_coin_sound()
    create_powerup_sound()
    create_damage_sound()
    create_victory_sound()
    create_game_over_sound()
    create_background_music()
    
    print("All sound effects created successfully!") 