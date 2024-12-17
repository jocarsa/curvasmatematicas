import cv2
import numpy as np
import math
import random

# Video settings
width, height = 1920, 1080  # Resolution
fps = 60                   # Frames per second
duration = 10              # Duration in seconds
output_file = 'superellipse_curve.mp4'

# Video writer setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# Time and scale settings
t_max = duration * fps     # Total number of frames
scale = 300                # Scale factor for curve rendering
center = (width // 2, height // 2)

# Randomize Superellipse (Lamé Curve) parameters
a = random.uniform(100, 300)  # Semi-major axis
b = random.uniform(100, 300)  # Semi-minor axis
n = random.uniform(2, 4)      # Exponent controlling the shape

# Function to compute Superellipse curve coordinates
def superellipse_curve(t):
    x = a * math.copysign(abs(math.cos(t)) ** (2 / n), math.cos(t))
    y = b * math.copysign(abs(math.sin(t)) ** (2 / n), math.sin(t))
    return x, y

# Framebuffer
points = []  # Store curve points incrementally
for i in range(t_max):
    frame = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
    
    # Compute the next point
    t = 2 * math.pi * (i / t_max)  # Full rotation
    x, y = superellipse_curve(t)
    x_pixel = int(center[0] + x)
    y_pixel = int(center[1] - y)
    
    if 0 <= x_pixel < width and 0 <= y_pixel < height:
        points.append((x_pixel, y_pixel))
    
    # Draw the curve incrementally
    for j in range(1, len(points)):
        cv2.line(frame, points[j-1], points[j], (0, 0, 0), 2)
    
    # Draw axes
    cv2.line(frame, (0, center[1]), (width, center[1]), (200, 200, 200), 1)
    cv2.line(frame, (center[0], 0), (center[0], height), (200, 200, 200), 1)

    # Display the frame
    cv2.imshow('Superellipse Curve', frame)
    video_writer.write(frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
video_writer.release()
cv2.destroyAllWindows()
print(f'Video saved as {output_file}')
