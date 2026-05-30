import pygame
import os
import numpy as np
from array import array
from math import sin, pi

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=1)
pygame.init()

# Create directories
os.makedirs("assets/sounds", exist_ok=True)

# Create a simple jump sound
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

# Create sound from buffer and save it
sound_file = os.path.join("assets", "sounds", "jump.wav")
with open(sound_file, 'wb') as f:
    # Write WAV header (very minimal version)
    f.write(b'RIFF')
    f.write((36 + len(buf) * 2).to_bytes(4, 'little'))  # File size - 8
    f.write(b'WAVEfmt ')
    f.write((16).to_bytes(4, 'little'))  # Format chunk size
    f.write((1).to_bytes(2, 'little'))  # Format (1 = PCM)
    f.write((1).to_bytes(2, 'little'))  # Channels
    f.write((sample_rate).to_bytes(4, 'little'))  # Sample rate
    f.write((sample_rate * 2).to_bytes(4, 'little'))  # Byte rate
    f.write((2).to_bytes(2, 'little'))  # Block align
    f.write((16).to_bytes(2, 'little'))  # Bits per sample
    f.write(b'data')
    f.write((len(buf) * 2).to_bytes(4, 'little'))  # Data chunk size
    
    # Write audio data
    for sample in buf:
        f.write(sample.to_bytes(2, 'little', signed=True))

print(f"Created {sound_file}")

# Also create empty placeholder files for other sounds
placeholder_sounds = ["coin.wav", "powerup.wav", "damage.wav", "victory.wav", "gameover.wav", "background_music.wav"]

for sound_name in placeholder_sounds:
    with open(os.path.join("assets", "sounds", sound_name), 'wb') as f:
        # Write minimal WAV header with almost no data
        f.write(b'RIFF')
        f.write((36 + 2).to_bytes(4, 'little'))
        f.write(b'WAVEfmt ')
        f.write((16).to_bytes(4, 'little'))
        f.write((1).to_bytes(2, 'little'))
        f.write((1).to_bytes(2, 'little'))
        f.write((sample_rate).to_bytes(4, 'little'))
        f.write((sample_rate * 2).to_bytes(4, 'little'))
        f.write((2).to_bytes(2, 'little'))
        f.write((16).to_bytes(2, 'little'))
        f.write(b'data')
        f.write((2).to_bytes(4, 'little'))
        f.write((0).to_bytes(2, 'little', signed=True))
    print(f"Created empty placeholder for {sound_name}")

print("All sound files created!") 