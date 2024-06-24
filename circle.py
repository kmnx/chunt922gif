import pygame
import sys

pygame.init()

# Screen dimensions
screen_width = 320
screen_height = 240
screen = pygame.display.set_mode((screen_width, screen_height),pygame.SCALED, pygame.DOUBLEBUF | pygame.HWSURFACE, vsync=1)

# Circle properties
circle_radius = 20
circle_color = (255, 0, 0)  # Red

# Initial circle position at the top of the screen, centered horizontally
circle_x = screen_width // 2 - circle_radius
circle_y = 0

# Create a Rect for the circle. The Rect is defined by its top-left corner, width, and height.
circle_rect = pygame.Rect(circle_x, circle_y, circle_radius * 2, circle_radius * 2)

# Scroll speed (pixels per second)
scroll_speed = 100

# Clock to control frame rate
clock = pygame.time.Clock()

# Initialize font module
pygame.font.init()
font = pygame.font.SysFont(None, 30)

# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Calculate delta time
    fps = clock.get_fps()
    print(fps)
    fps_text = font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update circle position by modifying the Rect
    circle_rect.y += scroll_speed * dt

    # Ensure the circle stays within screen bounds
    if circle_rect.top > screen_height:
        circle_rect.y = 0 - circle_rect.height

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the circle using the center of the Rect
    pygame.draw.circle(screen, circle_color, circle_rect.center, circle_radius)

    # Draw the FPS counter
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()