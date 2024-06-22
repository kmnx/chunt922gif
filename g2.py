import pygame
import os
from PIL import Image
import time

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

def display_gif_frames(frames, screen):
    for frame, duration in frames:
        surface = pil_image_to_surface(frame)
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        time.sleep(duration / 1000.0)  # Convert milliseconds to seconds

# Initialize Pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600), pygame.SCALED | pygame.DOUBLEBUF)
pygame.display.set_caption('GIF Sequence Display')

# Load GIFs
gif_dir = 'gifs'
gif_files = [f for f in os.listdir(gif_dir) if f.endswith('.gif')]
gif_frames_list = [load_gif_frames(os.path.join(gif_dir, gif)) for gif in gif_files]

# Main loop
running = True
gif_index = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gif_index = (gif_index + 1) % len(gif_frames_list)  # Loop back to first GIF
                display_gif_frames(gif_frames_list[gif_index], screen)

pygame.quit()