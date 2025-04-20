import cv2
import numpy as np
import math

# Video settings
width, height = 1920, 1080  # Resolution
fps = 60                   # Frames per second
duration = 60*60              # Duration in seconds
output_file = 'butterfly_curve_colorful.mp4'

# Video writer setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# Time and scale settings
t_max = duration * fps     # Total number of frames
scale = 150                # Scale factor for curve rendering
center = (width // 2, height // 2)

# Color function
def get_color(t, max_t):
    if max_t == 0:  # Prevent division by zero
        return (0, 0, 0)
    ratio = t / max_t
    r = int(128 + 127 * math.sin(2 * math.pi * ratio))
    g = int(128 + 127 * math.sin(2 * math.pi * ratio + 2))
    b = int(128 + 127 * math.sin(2 * math.pi * ratio + 4))
    return (b, g, r)

# Function to compute butterfly curve coordinates
def butterfly_curve(t):
    t = t / 60.0  # Adjust for smooth progression
    try:
        e_cost = math.exp(math.cos(t))
        cos_4t = math.cos(4 * t)
        sin_t12 = math.sin(t / 12) ** 5
        x = math.sin(t) * (e_cost - 2 * cos_4t - sin_t12)
        y = math.cos(t) * (e_cost - 2 * cos_4t - sin_t12)
    except (ValueError, OverflowError):
        return 0, 0  # Safe fallback for invalid values
    return x, y

# Create gradient background
def create_background(frame_num, total_frames):
    if total_frames == 0:  # Prevent division by zero
        total_frames = 1
    ratio = frame_num / total_frames
    gradient = np.linspace(0, 255, height, dtype=np.uint8)
    background = np.tile(gradient, (width, 1)).T
    colored_background = cv2.applyColorMap(background, cv2.COLORMAP_JET)
    return colored_background

# Frame buffer
previous_point = None
for i in range(t_max):
    frame = create_background(i, t_max)  # Gradient background
    curve_layer = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Draw the butterfly curve
    for t in np.linspace(0, max(i, 1), num=1000):  # Avoid invalid range
        x, y = butterfly_curve(t)
        x_pixel = int(center[0] + x * scale)
        y_pixel = int(center[1] - y * scale)
        color = get_color(t, max(i, 1))  # Avoid zero division
        
        if 0 <= x_pixel < width and 0 <= y_pixel < height:
            if previous_point is not None:
                cv2.line(curve_layer, previous_point, (x_pixel, y_pixel), color, 25)  # Thicker line
            previous_point = (x_pixel, y_pixel)
        else:
            previous_point = None

    # Blend curve and background
    blended_frame = cv2.addWeighted(frame, 0.7, curve_layer, 0.8, 0)

    # Draw axes
    cv2.line(blended_frame, (0, center[1]), (width, center[1]), (50, 50, 50), 1)
    cv2.line(blended_frame, (center[0], 0), (center[0], height), (50, 50, 50), 1)
    
    # Display the frame
    cv2.imshow('Butterfly Curve', blended_frame)
    video_writer.write(blended_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
video_writer.release()
cv2.destroyAllWindows()
print(f'Video saved as {output_file}')
