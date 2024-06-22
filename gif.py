import pygame
import os
from PIL import Image

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

# Set the display to fullscreen
info = pygame.display.Info()
screen = pygame.display.set_mode((320, 240))

#screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
pygame.display.set_caption('GIF Sequence Display')

# Load GIFs (assuming they are in the 'gifs' directory)
gif_dir = 'gifs'
gif_files = [f for f in os.listdir(gif_dir) if f.endswith('.gif')]
gif_frames = [load_gif_frames(os.path.join(gif_dir, gif)) for gif in gif_files]
# Add these variables before the main loop
slot_machine_effect = False
slot_machine_speed = 0.1  # Initial speed (in seconds)
slot_machine_max_speed = 0.5  # Max speed (in seconds)
slot_machine_acceleration = 1.1  # Acceleration factor
slot_machine_max_iterations = 20  # Maximum iterations before stopping



# Main loop
running = True
clock = pygame.time.Clock()
gif_index = 0
frame_index = 0
elapsed_time = 0
speed_modifier = 1.0  # Modifier for adjusting the playback speed

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Activate the slot machine effect
                slot_machine_effect = True
                slot_machine_speed = 0.1  # Reset speed
                slot_machine_iterations = 0  # Reset iterations
                frame_index = 0
                elapsed_time = 0
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                speed_modifier *= 1.1  # Increase speed
            elif event.y < 0:
                speed_modifier /= 1.1  # Decrease speed

    if slot_machine_effect:
        if slot_machine_iterations < slot_machine_max_iterations:
            # Display the first frame of the next GIF
            frame, duration = gif_frames[gif_index][0]
            scaled_frame = pygame.transform.scale(pil_image_to_surface(frame), (320, 240))
            screen.fill((0, 0, 0))
            screen.blit(scaled_frame, (0, 0))
            pygame.display.flip()

            # Increment the GIF index for the next iteration within the effect
            gif_index = (gif_index + 1) % len(gif_frames)

            # Increment and check the iteration counter
            slot_machine_iterations += 1

            # Control the speed of iteration
            pygame.time.wait(int(slot_machine_speed * 1000))
            slot_machine_speed = min(slot_machine_speed * slot_machine_acceleration, slot_machine_max_speed)
        else:
            slot_machine_effect = False  # Stop the slot machine effect
            frame_index = 0
            elapsed_time = 0
    else:
        # Normal GIF display logic
        frame, duration = gif_frames[gif_index][frame_index]
        scaled_frame = pygame.transform.scale(pil_image_to_surface(frame), (320, 240))
        screen.fill((0, 0, 0))
        screen.blit(scaled_frame, (0, 0))
        pygame.display.flip()

        elapsed_time += clock.get_time()
        if elapsed_time >= duration / speed_modifier:
            frame_index = (frame_index + 1) % len(gif_frames[gif_index])
            elapsed_time = 0

    clock.tick(60)

pygame.quit()
