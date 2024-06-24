import pygame
import sys

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 320
screen_height = 240
screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF | pygame.HWSURFACE, pygame.SCALED, vsync=1)

# Load the image
image = pygame.image.load('gifs/chatangosmile.png')
image_rect = image.get_rect()

# Set the initial position of the image (above the screen)
image_rect.y = -image_rect.height

# Set the scroll speed (pixels per frame)
scroll_speed = 1000
clock = pygame.time.Clock()
# Main loop
running = True
while running:
    # Handle events
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move the image down
    #prev_y = image_rect.y
    image_rect.y += scroll_speed * dt
    #print(image_rect.y)
    #if image_rect.y != prev_y+2:
    #    print("rahhhhhhh")


    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the image
    screen.blit(image, image_rect)

    # Update the display
    pygame.display.update()

    # Check if the image is completely off the screen
    if image_rect.y > screen_height:
        image_rect.y = -image_rect.height

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
