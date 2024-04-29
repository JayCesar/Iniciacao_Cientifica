import tkinter as tk
import random

def draw_line(canvas, points, color):
    # Draw line segments
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill=color, width=1.5)
    
    # Draw circles at each point
    for point in points:
        x, y = point
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")  # Adjust the size and color as needed

def ramer_douglas_peucker(points, epsilon):
    if len(points) < 3:
        return points

    max_distance = 0
    index = 0
    end = len(points) - 1

    for i in range(1, end):
        distance = perpendicular_distance(points[i], points[0], points[end])
        if distance > max_distance:
            index = i
            max_distance = distance

    simplified = []
    if max_distance > epsilon:
        left_part = ramer_douglas_peucker(points[:index + 1], epsilon)
        right_part = ramer_douglas_peucker(points[index:], epsilon)
        simplified = left_part[:-1] + right_part
    else:
        simplified = [points[0], points[end]]

    return simplified

def perpendicular_distance(point, line_start, line_end):
    x, y = point
    x1, y1 = line_start
    x2, y2 = line_end
    
    nominator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
    denominator = ((y2 - y1)**2 + (x2 - x1)**2)**0.5
    
    return nominator / denominator

def calculate_canvas_size(points):
    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_y = max(point[1] for point in points)

    canvas_width = max_x - min_x + 20  # Add padding of 10 pixels on each side
    canvas_height = max_y - min_y + 20  # Add padding of 10 pixels on each side

    return canvas_width, canvas_height

def calculate_epsilon(canvas_width, canvas_height, points):
    max_distance = 0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        distance = ((y2 - y1)**2 + (x2 - x1)**2)**0.5
        max_distance = max(max_distance, distance)
    return max(canvas_width, canvas_height) * 0.05 * (max_distance / (len(points) - 1))

def generate_random_points():
    points = []
    prev_x = 0
    for i in range(10):
        x = prev_x + random.randint(10, 100)
        y = random.randint(0, 800)
        points.append((x, y))
        prev_x = x
    
    # Add start and end points to ensure the entire range is covered
    points.insert(0, (0, 0))
    points.append((800, 800))
    
    return points

# Example points
points = [(1, 1), (3, 3), (4, 4), 
          (5, 5), (6, 6), (7, 200), 
          (15, 100), (16, 16), (100, 100), 
          (150, 10), (180, 200), (210, 120), (260, 280)]

# Calculate canvas size dynamically
canvas_width, canvas_height = calculate_canvas_size(points)

# Calculate epsilon based on canvas size and distance between points
epsilon = calculate_epsilon(canvas_width, canvas_height, points)

simplified_points = ramer_douglas_peucker(points, epsilon)
print("Pontos originais:", points)
print("Pontos simplificados:", simplified_points)

# Create the Tkinter window
root = tk.Tk()
root.title("Simplified Line with Points")

# Create a canvas widget
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Draw original and simplified lines and points
draw_line(canvas, points, "black")
draw_line(canvas, simplified_points, "blue")

# Run the Tkinter event loop
root.mainloop()