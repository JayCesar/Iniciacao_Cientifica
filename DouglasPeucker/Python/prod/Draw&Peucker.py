import tkinter as tk

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

# Exemple
points = [(1, 1), (3, 3), (4, 4), 
          (5, 5), (6, 6), (7, 200), 
          (15, 100), (16, 16), (100, 100), (150, 10), (180, 200), (210, 120), (260, 280)]

epsilon = 100

simplified_points = ramer_douglas_peucker(points, epsilon)
print("Pontos originais:", points)
print("Pontos simplificados:", simplified_points)

# Create the Tkinter window
root = tk.Tk()
root.title("Simplified Line with Points")

# Create a canvas widget
canvas = tk.Canvas(root, width=250, height=250)
canvas.pack()

# Draw simplified line and points
draw_line(canvas, points, "black")
draw_line(canvas, simplified_points, "blue")

# Run the Tkinter event loop
root.mainloop()
