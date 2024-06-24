import pygame
import os
from PIL import Image
import random

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

pygame.init()
screen = pygame.display.set_mode((960, 720), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption('GIF Sequence Display')
current_gif_indices = [0, 0, 0]  # Indices for each GIF
frame_positions = [-240, -240, -240]  # Initial y-positions for each GIF



all_first_frames = load_all_first_frames(gif_paths)
pre_scaled_frames = [pygame.transform.scale(pil_image_to_surface(frame), (320, 240)) for frame, _ in all_first_frames]

slot_machine_effect = False
slot_machine_speed = 0.1
slot_machine_iterations = 0
slot_machine_max_iterations = 20

running = True
clock = pygame.time.Clock()
frame_positions = [-240]
gif_index = 0
frame_index = 0
elapsed_time = 0
speed_modifier = 1.0  # Playback speed modifier


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

    


    screen.fill((0, 0, 0))
    
    if slot_machine_effect:
        if 'random_gif_indices' not in globals() or len(random_gif_indices) != 20:
            random_gif_indices = random.sample(range(len(pre_scaled_frames)), 20)
            current_gif_index = 0

        frame_index = random_gif_indices[current_gif_index % 20]
        scaled_frame = pre_scaled_frames[frame_index]
        y_position = frame_positions[0]

        screen.blit(scaled_frame, (0, y_position))
        frame_positions[0] += 40

        if y_position >= 240:
            frame_positions[0] = -240
            current_gif_index += 1

        pygame.display.flip()
        
        if frame_positions[0] == 0:
            slot_machine_iterations += 1
            if slot_machine_iterations >= slot_machine_max_iterations:
                slot_machine_effect = False
                frame_positions = [-240]
                gif_index = random_gif_indices[current_gif_index % 20]
                del random_gif_indices
    else:
        gif_all_frames = load_gif_frames(gif_paths[gif_index])
        frame, duration = gif_all_frames[frame_index]
        scaled_frame = pygame.transform.scale(pil_image_to_surface(frame), (320, 240))
        
        screen.blit(scaled_frame, (0, 0))
        pygame.display.flip()
        elapsed_time += clock.get_time()
        if elapsed_time >= duration:
            frame_index = (frame_index + 1) % len(gif_all_frames)
            elapsed_time = 0

    clock.tick(60)

pygame.quit()
