```python
import time
import math
import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_letter_A(cx, cy, size=1):
    points = set()
    height = int(8 * size)
    width = int(6 * size)
    
    for row in range(height):
        progress = row / height
        left_x = cx - width // 2 + int(progress * width // 2)
        right_x = cx + width // 2 - int(progress * width // 2)
        points.add((int(left_x), cy - height // 2 + row))
        points.add((int(right_x), cy - height // 2 + row))
        
        if abs(progress - 0.5) < 0.1:
            for x in range(int(left_x), int(right_x) + 1):
                points.add((x, cy - height // 2 + row))
    
    return points

def get_letter_I(cx, cy, size=1):
    points = set()
    height = int(8 * size)
    width = int(4 * size)
    
    for x in range(cx - width // 2, cx + width // 2 + 1):
        points.add((x, cy - height // 2))
        points.add((x, cy + height // 2))
    
    for y in range(cy - height // 2, cy + height // 2 + 1):
        points.add((cx, y))
    
    return points

def rotate_point(x, y, cx, cy, angle):
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    dx = x - cx
    dy = y - cy
    
    new_x = dx * cos_a - dy * sin_a + cx
    new_y = dx * sin_a + dy * cos_a + cy
    
    return new_x, new_y

def render_frame(angle, width=80, height=40):
    canvas = [[' ' for _ in range(width)] for _ in range(height)]
    
    center_x = width // 2
    center_y = height // 2
    
    a_cx = center_x - 8
    a_cy = center_y
    i_cx = center_x + 8
    i_cy = center_y
    
    pivot_x = center_x
    pivot_y = center_y
    
    a_points = get_letter_A(a_cx, a_cy, size=1.5)
    i_points = get_letter_I(i_cx, i_cy, size=1.5)
    
    all_points = list(a_points) + list(i_points)
    
    chars = ['*', '+', 'o', '@', '#', '•']
    char_index = int(angle / 60) % len(chars)
    char = chars[char_index]
    
    for x, y in all_points:
        rx, ry = rotate_point(x, y, pivot_x, pivot_y, angle)
        ix, iy = int(round(rx)), int(round(ry))
        
        if 0 <= ix < width and 0 <= iy < height:
            canvas[iy][ix] = char
    
    return '\n'.join(''.join(row) for row in canvas)

def spin_ai():
    angle = 0
    try:
        while True:
            clear_screen()
            frame = render_frame(angle)
            print(frame)
            print(f"\n  [ Spinning AI ] angle: {angle:3d}°")
            
            angle = (angle + 5) % 360
            time.sleep(0.05)
    except KeyboardInterrupt:
        clear_screen()
        print("Stopped spinning.")

if __name__ == "__main__":
    spin_ai()
```