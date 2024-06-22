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

# Assuming these variables are defined and initialized appropriately
num_frames_to_display = 20  # Number of frames to display at once
frame_spacing = 10  # Space between frames
frame_positions = [-240 - i * (240 + frame_spacing) for i in range(num_frames_to_display)]  # Initial Y-positions for each frame


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
        screen.fill((0, 0, 0))  # Clear the screen

        for i in range(num_frames_to_display):
            # Calculate the index of the next frame to display
            frame_index = (gif_index + i) % len(gif_frames)
            frame, _ = gif_frames[frame_index][0]  # Assuming we always show the first frame of each GIF for simplicity

            # Calculate the Y-position for the current frame
            y_position = frame_positions[i]

            # Display the frame at its current position
            scaled_frame = pygame.transform.scale(pil_image_to_surface(frame), (320, 240))
            screen.blit(scaled_frame, (0, y_position))

            # Update the Y-position for the next iteration
            frame_positions[i] += 5  # Adjust this value to control the speed of the scrolling

            # Reset the position of the frame if it moves out of the visible area
            if y_position >= 240 + (num_frames_to_display - 1) * (240 + frame_spacing):
                frame_positions[i] = -240 - frame_spacing

        pygame.display.flip()

        # Check if the last frame has moved out of the visible area before incrementing slot_machine_iterations
        if frame_positions[-1] >= 240:
            slot_machine_iterations += 1
            if slot_machine_iterations >= slot_machine_max_iterations:
                slot_machine_effect = False
                # Reset positions and other necessary variables
                frame_positions = [-240 - i * (240 + frame_spacing) for i in range(num_frames_to_display)]
                # Other reset logic here
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
