import pygame
import sys
import os
from PIL import Image

# Load all first frames from GIFs
def load_all_first_frames(gif_paths):
    first_frames = []
    for gif in gif_paths:
        with Image.open(gif) as image:
            frame = image.copy().convert('RGBA')
            duration = image.info.get('duration', 100)
            first_frames.append((frame, duration))
    return first_frames

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((320, 240),pygame.SCALED, pygame.DOUBLEBUF | pygame.HWSURFACE, vsync=1)

# Load the static image
image_path = './gifs/chatangosmile.png'  # Replace with your image path
image = pygame.image.load(image_path).convert_alpha()  # Convert outside the loop
image_y = -240  # Start above the screen

# Main loop setup
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(360) / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Update image position with delta time
    image_y += 100 * dt  # Adjust speed as needed, 100 pixels per second
    if image_y > 240:
        image_y = -240  # Reset to start above the screen

    # Draw the image
    screen.blit(image, (0, image_y))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()