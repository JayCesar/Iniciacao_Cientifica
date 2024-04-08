from tkinter import *

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

# Example usage
points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), 
          (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), 
          (15, 15), (16, 16), (17, 17), (18, 18), (19, 19)]
# points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

epsilon = 0.2

simplified_points = ramer_douglas_peucker(points, epsilon)
# print("Pontos originais:", points)
# print("Pontos simplificados:", simplified_points)

# Create the Tkinter window
my_window = Tk()
# my_window.title("Simplified Line")
my_canvas = Canvas(my_window, width=400, height=400, background='white')
my_canvas.grid(row=0, column=0)
# my_canvas.create_line(0,0,400,400,fill='black')
# Create a canvas widget
# canvas = tk.Canvas(root, width=500, height=500)
# canvas.pack()

for i in range(len(points) - 1):
    print(i)

# Draw simplified line
# draw_line(canvas, points)

# Run the Tkinter event loop
my_canvas.mainloop()
