import cv2
import numpy as np
import math
import random

# Video settings
width, height = 1920, 1080  # Resolution
fps = 60                   # Frames per second
duration = 10              # Duration in seconds
output_file = 'lemniscate_curve.mp4'

# Video writer setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# Time and scale settings
t_max = duration * fps     # Total number of frames
scale = 300                # Scale factor for curve rendering
center = (width // 2, height // 2)

# Lemniscate of Bernoulli parameters
a = random.uniform(100, 300)  # Random scale factor

# Function to compute Lemniscate of Bernoulli coordinates
def lemniscate_curve(t):
    cos_2t = math.cos(2 * t)
    if cos_2t < 0:  # Ensure valid square root
        return None, None
    r = a * math.sqrt(cos_2t)
    x = r * math.cos(t)
    y = r * math.sin(t)
    return x, y

# Framebuffer
points = []  # Store curve points incrementally
for i in range(t_max):
    frame = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
    
    # Compute the next point
    t = 2 * math.pi * (i / t_max)  # Full rotation
    x, y = lemniscate_curve(t)
    if x is None or y is None:
        continue
    x_pixel = int(center[0] + x)
    y_pixel = int(center[1] - y)
    
    if 0 <= x_pixel < width and 0 <= y_pixel < height:
        points.append((x_pixel, y_pixel))
    
    # Draw the curve incrementally
    for j in range(1, len(points)):
        cv2.line(frame, points[j-1], points[j], (0, 0, 0), 1)
    
    # Draw axes
    cv2.line(frame, (0, center[1]), (width, center[1]), (200, 200, 200), 1)
    cv2.line(frame, (center[0], 0), (center[0], height), (200, 200, 200), 1)

    # Display the frame
    cv2.imshow('Lemniscate of Bernoulli', frame)
    video_writer.write(frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
video_writer.release()
cv2.destroyAllWindows()
print(f'Video saved as {output_file}')
