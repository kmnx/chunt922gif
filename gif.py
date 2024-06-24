# Import necessary libraries
import pygame
import os
from PIL import Image
import random

gif_dir = 'gifs'
gif_paths = [os.path.join(gif_dir, f) for f in os.listdir(gif_dir) if f.endswith('.gif')]

# Function to load the first frame of a GIF
def load_first_frame(gif_path):
    with Image.open(gif_path) as image:
        frame = image.copy().convert('RGBA')
        duration = image.info.get('duration', 100)  # Default duration if not specified
    return frame, duration

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

# Function to convert PIL image to Pygame surface
def pil_image_to_surface(pil_image):
    mode = pil_image.mode
    size = pil_image.size
    data = pil_image.tobytes()
    return pygame.image.fromstring(data, size, mode)

# Initialize Pygame
pygame.init()

# Set the display size
screen = pygame.display.set_mode((320, 240))
pygame.display.set_caption('GIF Sequence Display')

# Load GIFs from the 'gifs' directory
#gif_dir = 'gifs'
#gif_files = [f for f in os.listdir(gif_dir) if f.endswith('.gif')]
#gif_frames = [load_gif_frames(os.path.join(gif_dir, gif)) for gif in gif_files]
all_first_frames = load_all_first_frames(gif_paths)

# Variables for slot machine effect
slot_machine_effect = False
slot_machine_speed = 0.9  # Initial speed (in seconds)
slot_machine_iterations = 0

slot_machine_max_iterations = 20  # Maximum iterations before stopping

# Main loop variables
running = True
clock = pygame.time.Clock()
gif_index = 0
frame_index = 0
elapsed_time = 0
speed_modifier = 1.0  # Playback speed modifier

# Variables for displaying multiple frames
num_frames_to_display = 1  # Number of frames to display at once
frame_spacing = 10  # Space between frames
frame_positions = [-240 - i * (240 + frame_spacing) for i in range(num_frames_to_display)]
last_frame_index = 0
last_frame_index = 0
#last_frame_duration = gif_frames[gif_index][1]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Activate/deactivate the slot machine effect
                slot_machine_effect = not slot_machine_effect
                slot_machine_speed = 0.1  # Reset speed
                slot_machine_iterations = 0  # Reset iterations
                frame_index = 0
                elapsed_time = 0
        elif event.type == pygame.MOUSEWHEEL:
            # Adjust speed modifier based on mouse wheel movement
            if event.y > 0:
                speed_modifier *= 1.1
            elif event.y < 0:
                speed_modifier /= 1.1

    if slot_machine_effect:
        current_speed = max(1, 10 - slot_machine_iterations)
        if 'random_gif_indices' not in globals() or len(random_gif_indices) != 20:
            # Select 20 unique random indices from gif_frames
            random_gif_indices = random.sample(range(len(all_first_frames)), 20)
            current_gif_index = 0  # Initialize a counter to keep track of the current GIF being displayed

        screen.fill((0, 0, 0))  # Clear the screen
        # Use the current index for the slot machine effect
        frame_index = random_gif_indices[current_gif_index % 20]
        frame, _ = all_first_frames[frame_index]
        y_position = frame_positions[0]
        scaled_frame = pygame.transform.scale(pil_image_to_surface(frame), (320, 240))
        screen.blit(scaled_frame, (0, y_position))
        frame_positions[0] += 20  # Update Y-position
        if y_position >= 240:
            frame_positions[0] = -240 
            # Move to the next GIF after the current one moves off-screen
            current_gif_index += 1
            #if current_gif_index >= 20:  # Reset if we've displayed all 20 GIFs
            #    current_gif_index = 0

        pygame.display.flip()
        if frame_positions[0] == 0:
            slot_machine_iterations += 1
            if slot_machine_iterations >= slot_machine_max_iterations:
                slot_machine_effect = False
                frame_positions = [-240 - frame_spacing]  # Reset frame position
                # Set gif_index to the last index from random_gif_indices to continue displaying the last GIF
                gif_index = random_gif_indices[current_gif_index % 20]
                #last_frame_index = gif_index
                frame_index = 0  # Assuming gif_index is the frame index
                #last_frame_duration = gif_frames[gif_index][1]                 
                del random_gif_indices
    else:
        # Normal GIF display logic
        gif_all_frames = load_gif_frames(gif_paths[gif_index])
        frame, duration = gif_all_frames[frame_index]
        scaled_frame = pygame.transform.scale(pil_image_to_surface(frame), (320, 240))
        screen.fill((0, 0, 0))
        screen.blit(scaled_frame, (0, 0))
        pygame.display.flip()
        elapsed_time += clock.get_time()
        if elapsed_time >= duration / speed_modifier:
            frame_index = (frame_index + 1) % len(gif_all_frames)
            elapsed_time = 0

    clock.tick(60)

pygame.quit()