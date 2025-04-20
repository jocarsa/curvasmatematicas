import cv2
import numpy as np
import math
import random
import time

for _ in range(0,10):

    # Video settings
    width, height = 1920, 1080  # Resolution
    fps = 60                   # Frames per second
    duration_per_sim = 60*60      # Duration of each simulation in seconds
    num_simulations = 10       # Number of simulations
    output_file = 'colorful_epicycloid_curve_incremental.mp4'

    # Video writer setup
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Time and scale settings
    frames_per_sim = duration_per_sim * fps  # Total number of frames per simulation
    center = (width // 2, height // 2)

    # Function to compute Epicycloid curve coordinates
    def epicycloid_curve(t, R, r):
        x = (R + r) * math.cos(t) - r * math.cos(((R + r) / r) * t)
        y = (R + r) * math.sin(t) - r * math.sin(((R + r) / r) * t)
        return x, y

    # Color function
    def get_color(frame_index):
        """
        Generate a cycling color based on the frame index.
        Color changes are independent of the animation duration.
        """
        cycle_speed = 0.1  # Adjust this value to control how fast colors change
        r = int(128 + 127 * math.sin(cycle_speed * frame_index))
        g = int(128 + 127 * math.sin(cycle_speed * frame_index + 2))
        b = int(128 + 127 * math.sin(cycle_speed * frame_index + 4))
        return (b, g, r)

    # Create gradient background
    def create_background():
        return np.zeros((height, width, 3), dtype=np.uint8)

    # Main simulation loop
    for sim in range(num_simulations):
        # Randomize Epicycloid curve parameters for each simulation
        R = random.uniform(50, 200)        # Radius of the fixed circle
        r = random.uniform(10, 100)        # Radius of the rolling circle
        scale = 100                        # Initial scale factor for curve rendering

        # Framebuffer
        curve_layer = create_background()

        # Initialize the first point
        prev_x, prev_y = None, None

        for i in range(frames_per_sim):
            scale += 0.001

            # Compute the next point
            t = 2 * math.pi * (i / fps) / 5  # Scale t to generate more loops
            x, y = epicycloid_curve(t, R, r)
            x_pixel = int(center[0] + x * scale / R)
            y_pixel = int(center[1] - y * scale / R)

            # Draw only the new segment if valid
            if prev_x is not None and 0 <= x_pixel < width and 0 <= y_pixel < height:
                color = get_color(i)  # Use frame index for independent color cycling
                cv2.line(curve_layer, (prev_x, prev_y), (x_pixel, y_pixel), color, 20)

            # Update the previous point
            prev_x, prev_y = x_pixel, y_pixel

            # Display and save the frame
            cv2.imshow('Colorful Epicycloid Curve', curve_layer)
            video_writer.write(curve_layer)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Clean up
    video_writer.release()
    cv2.destroyAllWindows()
    print(f'Video saved as {output_file}')
