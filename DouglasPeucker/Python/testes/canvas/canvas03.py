import tkinter as tk

def douglas_peucker(points, tolerance):
    if len(points) <= 2:
        return points

    max_distance = 0
    index = 0
    end = len(points) - 1

    for i in range(1, end):
        distance = perpendicularDistance(points[i], points[0], points[end])
        if distance > max_distance:
            index = i
            max_distance = distance

    if max_distance > tolerance:
        left_part = douglas_peucker(points[:index + 1], tolerance)
        right_part = douglas_peucker(points[index:], tolerance)
        return left_part[:-1] + right_part
    else:
        return [points[0], points[end]]

def perpendicularDistance(point, line_start, line_end):
    x, y = point
    x1, y1 = line_start
    x2, y2 = line_end
    nominator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
    denominator = ((y2 - y1) * 2 + (x2 - x1) * 2) ** 0.5
    return nominator / denominator

# Example usage
# points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
# points = [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)]
points = [(0, 0), (0.5, 0.5), (1, 1), (1.5, 1.5), (2, 2), (2.5, 2.5), (3, 3), (3.5, 3.5), (4, 4)]
points = [(0, 0), (0.5, 0.5), (1, 1), (1.5, 1.5), (2, 2), (2.5, 2.5), (3, 3), (3.5, 3.5), (4, 4)]


tolerance = 1
simplified_points = douglas_peucker(points, tolerance)

# Create the main window
root = tk.Tk()
root.title("Line Graph")

# Create a canvas to draw on
canvas_width = 500
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Scale the points to fit the canvas
max_x = max([x for x, y in simplified_points])
max_y = max([y for x, y in simplified_points])
scale_x = canvas_width / (max_x + 1)
scale_y = canvas_height / (max_y + 1)

# Draw the line
canvas.create_line([(scale_x * x, canvas_height - scale_y * y) for x, y in simplified_points], smooth=False, width=2)

# Draw the axes
canvas.create_line(0, canvas_height, canvas_width, canvas_height, arrow=tk.LAST)  # X-axis
canvas.create_line(0, 0, 0, canvas_height, arrow=tk.LAST)  # Y-axis

# Label the axes
canvas.create_text(canvas_width / 2, canvas_height + 20, text="X")
canvas.create_text(-20, canvas_height / 2, text="Y", angle=90)



# Run the main loop
root.mainloop()