import cv2
import numpy as np
import math
import random
import time
for _ in range(0,10):
    # Video settings
    width, height = 1920, 1080  # Resolution
    fps = 60                   # Frames per second
    duration = 60*60*12              # Duration in seconds
    output_file = 'colorful_epicycloid_curve'+str(round(time.time()))+'.mp4'

    # Video writer setup
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Time and scale settings
    t_max = duration * fps     # Total number of frames
    scale = 200                # Scale factor for curve rendering
    center = (width // 2, height // 2)

    # Randomize Epicycloid curve parameters
    R = random.uniform(50, 200)        # Radius of the fixed circle
    r = random.uniform(10, 100)        # Radius of the rolling circle

    # Function to compute Epicycloid curve coordinates
    def epicycloid_curve(t):
        x = (R + r) * math.cos(t) - r * math.cos(((R + r) / r) * t)
        y = (R + r) * math.sin(t) - r * math.sin(((R + r) / r) * t)
        return x, y

    # Color function
    def get_color(t, max_t):
        if max_t == 0:
            return (0, 0, 0)
        ratio = t / max_t
        r = int(128 + 127 * math.sin(2 * math.pi * ratio))
        g = int(128 + 127 * math.sin(2 * math.pi * ratio + 2))
        b = int(128 + 127 * math.sin(2 * math.pi * ratio + 4))
        return (b, g, r)

    # Create gradient background
    def create_background(frame_num, total_frames):
        if total_frames == 0:
            total_frames = 1
        ratio = frame_num / total_frames
        gradient = np.linspace(0, 255, height, dtype=np.uint8)
        background = np.tile(gradient, (width, 1)).T
        colored_background = cv2.applyColorMap(background, cv2.COLORMAP_TWILIGHT)
        return colored_background

    # Framebuffer
    points = []
    curve_layer = np.zeros((height, width, 3), dtype=np.uint8)

    for i in range(t_max):
        # Generate gradient background
        frame = create_background(i, t_max)

        # Compute the next point
        t = 2 * math.pi * (i / fps)/5  # Scale t to generate more loops
        x, y = epicycloid_curve(t)
        x_pixel = int(center[0] + x * scale / R)
        y_pixel = int(center[1] - y * scale / R)

        # Add points to the curve layer
        if 0 <= x_pixel < width and 0 <= y_pixel < height:
            points.append((x_pixel, y_pixel))

        # Draw the curve incrementally
        for j in range(1, len(points)):
            color = get_color(j, len(points))
            cv2.line(curve_layer, points[j - 1], points[j], color, 20)

        # Blend the curve layer with the background
        blended_frame = cv2.addWeighted(frame, 0.6, curve_layer, 0.8, 0)

        # Draw axes for reference
        cv2.line(blended_frame, (0, center[1]), (width, center[1]), (200, 200, 200), 1)
        cv2.line(blended_frame, (center[0], 0), (center[0], height), (200, 200, 200), 1)

        # Display and save the frame
        cv2.imshow('Colorful Epicycloid Curve', blended_frame)
        video_writer.write(blended_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    video_writer.release()
    cv2.destroyAllWindows()
    print(f'Video saved as {output_file}')
