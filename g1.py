import pygame
import os
from PIL import Image

def load_gif_frames(gif_path):
    image = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = image.copy().convert('RGBA')
            frames.append((frame, image.info['duration']))
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

# Set the display to fullscreen
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
pygame.display.set_caption('GIF Sequence Display')

# Load GIFs (assuming they are in the 'gifs' directory)
gif_dir = 'gifs'
gif_files = [f for f in os.listdir(gif_dir) if f.endswith('.gif')]
gif_frames = [load_gif_frames(os.path.join(gif_dir, gif)) for gif in gif_files]

# Main loop
running = True
clock = pygame.time.Clock()
gif_index = 0
frame_index = 0
elapsed_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Display the current GIF frame
    frame, duration = gif_frames[gif_index][frame_index]
    screen.fill((0, 0, 0))  # Clear the screen with black
    screen.blit(pil_image_to_surface(frame), (0, 0))
    pygame.display.flip()

    # Track the elapsed time and advance to the next frame if needed
    elapsed_time += clock.get_time()
    if elapsed_time >= duration:
        frame_index = (frame_index + 1) % len(gif_frames[gif_index])
        elapsed_time = 0
        if frame_index == 0:
            gif_index = (gif_index + 1) % len(gif_frames)

    # Control the frame rate
    clock.tick(60)

pygame.quit()
