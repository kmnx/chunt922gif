import pygame
import random
import os
from PIL import Image


gif_dir = 'gifs'
gif_paths = [os.path.join(gif_dir, f) for f in os.listdir(gif_dir) if f.endswith('.gif')]

def load_all_first_frames(gif_paths):
    first_frames = []
    for gif in gif_paths:
        with Image.open(gif) as image:
            frame = image.copy().convert('RGBA')
            duration = image.info.get('duration', 100)
            first_frames.append((frame, duration))
    return first_frames

# Function to load GIF frames
def load_gif_frames(gif_path, default_duration=100):
    image = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = image.copy().convert('RGBA')
            duration = image.info.get('duration', default_duration)
            frames.append((frame, duration))
            image.seek(image.tell() + 1)
    except EOFError:
        pass
    return frames

def pil_image_to_surface(pil_image):
    mode = pil_image.mode
    size = pil_image.size
    data = pil_image.tobytes()
    return pygame.image.fromstring(data, size, mode)

# Initialize Pygame
pygame.init()

# Set screen size
screen = pygame.display.set_mode((960, 720))

# Assuming pre_scaled_frames is a list of pre-scaled frames to 320x240
pre_scaled_frames = []  # This should be populated with your scaled frames
all_first_frames = load_all_first_frames(gif_paths)
pre_scaled_frames = [pygame.transform.scale(pil_image_to_surface(frame), (320, 240)) for frame, _ in all_first_frames]

# Variables for slot machine effect
slot_machine_effect = False
slot_machine_speed = 0.1
slot_machine_iterations = 0
slot_machine_max_iterations = 5  # Adjust as needed

# Initialize positions and indices for three GIFs
frame_positions = [-240, -240, -240]  # Starting y-positions for each GIF
current_gif_indices = [0, 0, 0]  # Current GIF index for each slot
random_gif_indices = []  # Will hold random sequence of indices for GIF frames

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                slot_machine_effect = not slot_machine_effect
                slot_machine_speed = 0.1
                slot_machine_iterations = 0
                # Reset for new effect
                frame_positions = [-240, -240, -240]
                current_gif_indices = [0, 0, 0]
                random_gif_indices = random.sample(range(len(pre_scaled_frames)), 20)

    screen.fill((0, 0, 0))

    if slot_machine_effect:
        for i in range(3):  # Adjust for three GIFs
            if not random_gif_indices:  # Ensure random_gif_indices is populated
                random_gif_indices = random.sample(range(len(pre_scaled_frames)), 20)
            
            frame_index = random_gif_indices[current_gif_indices[i] % 20]
            scaled_frame = pre_scaled_frames[frame_index]
            y_position = frame_positions[i]

            screen.blit(scaled_frame, (i * 320, y_position))  # Position GIFs next to each other
            frame_positions[i] += 40  # Scroll speed

            if y_position >= 720:
                frame_positions[i] = -240  # Reset position after scrolling off screen
                current_gif_indices[i] += 1  # Move to next GIF frame

        pygame.display.flip()

        # Check if all GIFs have reset to start a new iteration
        if all(pos >= 720 for pos in frame_positions):
            slot_machine_iterations += 1
            if slot_machine_iterations >= slot_machine_max_iterations:
                slot_machine_effect = False
                # Reset positions and indices for a new effect
                frame_positions = [-240, -240, -240]
                current_gif_indices = [0, 0, 0]
                random_gif_indices = []

pygame.quit()