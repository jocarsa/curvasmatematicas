import cv2
import numpy as np
import math

# Video settings
width, height = 1920, 1080  # Resolution
fps = 60                   # Frames per second
segundos = 60
minutos = 60
duration = fps*segundos*minutos            # Duration in seconds
output_file = 'butterfly_curve.mp4'

# Video writer setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# Time and scale settings
t_max = duration * fps     # Total number of frames
scale = 100                # Scale factor for curve rendering
center = (width // 2, height // 2)

# Function to compute butterfly curve coordinates
def butterfly_curve(t):
    t = t / 60.0  # Adjust for smooth progression
    e_cost = math.exp(math.cos(t))
    cos_4t = math.cos(4 * t)
    sin_t12 = math.sin(t / 12) ** 5
    
    x = math.sin(t) * (e_cost - 2 * cos_4t - sin_t12)
    y = math.cos(t) * (e_cost - 2 * cos_4t - sin_t12)
    return x, y

# Framebuffer
previous_point = None
for i in range(t_max):
    frame = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
    
    for t in np.linspace(0, i, num=i):
        x, y = butterfly_curve(t)
        x_pixel = int(center[0] + x * scale)
        y_pixel = int(center[1] - y * scale)
        
        if 0 <= x_pixel < width and 0 <= y_pixel < height:
            if previous_point is not None:
                cv2.line(frame, previous_point, (x_pixel, y_pixel), (0, 0, 0), 1)  # Draw black line
            previous_point = (x_pixel, y_pixel)
        else:
            previous_point = None

    # Draw axes
    cv2.line(frame, (0, center[1]), (width, center[1]), (200, 200, 200), 1)
    cv2.line(frame, (center[0], 0), (center[0], height), (200, 200, 200), 1)

    # Display the frame
    cv2.imshow('Butterfly Curve', frame)
    video_writer.write(frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
video_writer.release()
cv2.destroyAllWindows()
print(f'Video saved as {output_file}')
