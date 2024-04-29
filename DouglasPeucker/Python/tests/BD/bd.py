import tkinter as tk
import random
import psycopg2

# Establish a connection to your PostgreSQL database
conn = psycopg2.connect(
    database="rdp_storage",
    host="localhost",
    user="postgres",
    password="123456",
    port="5432"
)

def generate_random_points(dimension):
    points = []
    prev_x = 0
    for i in range(10):
        x = prev_x + random.randint(10, 100)  
        y = random.randint(0, dimension)
        points.append((x, y))
        prev_x = x

    points.insert(0, (0, 0))
    points.append((dimension, dimension))

    return points

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

def insert_non_simplified_points(points):
    cur = conn.cursor()
    # Delete data first
    cur.execute("DELETE FROM simplified_points")
    cur.execute("DELETE FROM non_simplified_points")
    for point in points:
        x, y = point
        sql = "INSERT INTO non_simplified_points (nome, ponto) VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))"
        data = (f"Point ({x}, {y})", x, y)
        cur.execute(sql, data)
    conn.commit()
    cur.close()

def insert_simplified_points(simplified_points, non_simplified_id):
    cur = conn.cursor()
    for point in simplified_points:
        x, y = point
        sql = "INSERT INTO simplified_points (simplified_nome, simplified_ponto, non_simplified_id) VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s)"
        data = (f"Simplified Point ({x}, {y})", x, y, non_simplified_id)
        cur.execute(sql, data)
    conn.commit()
    cur.close()

def calculate_canvas_size(points):
    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_y = max(point[1] for point in points)

    canvas_width = max_x - min_x + 20  
    canvas_height = max_y - min_y + 20  

    print("Canvas dimension: ", canvas_width, "x", canvas_height)

    return canvas_width, canvas_height


def calculate_epsilon(canvas_width, canvas_height, points):
    max_distance = 0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        distance = ((y2 - y1)**2 + (x2 - x1)**2)**0.5
        max_distance = max(max_distance, distance)
    return max(canvas_width, canvas_height) * 0.005 * (max_distance / (len(points) - 1)) 
# This data changes as the number of points

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

def appFunction(points, canvas_width, canvas_height):
    epsilon = calculate_epsilon(canvas_width, canvas_height, points)

    simplified_points = ramer_douglas_peucker(points, epsilon)

    # Insert non-simplified points into the database
    insert_non_simplified_points(points)

    # Retrieve the ID of the last inserted non-simplified point
    cur = conn.cursor()
    cur.execute("SELECT MAX(id) FROM non_simplified_points")
    non_simplified_id = cur.fetchone()[0]
    cur.close()

    # Insert simplified points with reference to the non-simplified point
    insert_simplified_points(simplified_points, non_simplified_id)

    # Create the Tkinter window
    root = tk.Tk()
    root.title("Simplified Line with Points")

    # Create a canvas widget
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # Draw original and simplified lines and points
    draw_line(canvas, points, "black")
    draw_line(canvas, simplified_points, "blue")
    print(points)

    # Run the Tkinter event loop
    root.mainloop()

# Define remaining functions (calculate_canvas_size, calculate_epsilon, draw_line) as per the previous code

# Example usage:
points = generate_random_points(300)
canvas_width, canvas_height = calculate_canvas_size(points)
appFunction(points, canvas_width, canvas_height)

# Close the database connection at the end
conn.close()
