import cv2
import numpy as np
import math
import random

# Video settings
width, height = 1920, 1080  # Resolution
fps = 60                   # Frames per second
duration = 10              # Duration in seconds
output_file = 'harmonograph_curve.mp4'

# Video writer setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# Time and scale settings
t_max = duration * fps     # Total number of frames
scale = 100                # Scale factor for curve rendering
center = (width // 2, height // 2)

# Randomize Harmonograph parameters
A1, A2 = random.uniform(50, 150), random.uniform(50, 150)  # Amplitudes
f1, f2 = random.uniform(0.5, 2), random.uniform(0.5, 2)   # Frequencies
d1, d2 = random.uniform(0.01, 0.05), random.uniform(0.01, 0.05)  # Dampening factors
p1, p2 = random.uniform(0, math.pi), random.uniform(0, math.pi)  # Phase shifts

# Function to compute Harmonograph curve coordinates
def harmonograph_curve(t):
    x = A1 * math.sin(f1 * t + p1) * math.exp(-d1 * t)
    y = A2 * math.sin(f2 * t + p2) * math.exp(-d2 * t)
    return x, y

# Framebuffer
points = []  # Store curve points incrementally
for i in range(t_max):
    frame = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
    
    # Compute the next point
    t = i / fps  # Time in seconds
    x, y = harmonograph_curve(t)
    x_pixel = int(center[0] + x * scale)
    y_pixel = int(center[1] - y * scale)
    
    if 0 <= x_pixel < width and 0 <= y_pixel < height:
        points.append((x_pixel, y_pixel))
    
    # Draw the curve incrementally
    for j in range(1, len(points)):
        cv2.line(frame, points[j-1], points[j], (0, 0, 0), 1)
    
    # Draw axes
    cv2.line(frame, (0, center[1]), (width, center[1]), (200, 200, 200), 1)
    cv2.line(frame, (center[0], 0), (center[0], height), (200, 200, 200), 1)

    # Display the frame
    cv2.imshow('Harmonograph Curve', frame)
    video_writer.write(frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
video_writer.release()
cv2.destroyAllWindows()
print(f'Video saved as {output_file}')
