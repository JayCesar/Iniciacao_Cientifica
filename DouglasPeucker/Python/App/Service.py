import tkinter as tk
import random
import psycopg2

def criar_conexao():
    try:
        # Estabelece a conexão com o banco de dados PostgreSQL
        conexao = psycopg2.connect(database="rdp_storage",
                                   host="localhost",
                                   user="postgres",
                                   password="123456",
                                   port="5432")
        print("Conexão PostgreSQL estabelecida com sucesso.\n")
        return conexao  # Retorna a conexão estabelecida

    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados PostgreSQL:", e)
        return None  # Retorna None se a conexão falhar

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

def create_non_simplified_table(table_name):
    try:
        conn = criar_conexao()
        cur = conn.cursor()

        # Call the stored procedure function
        cur.execute("SELECT create_non_simplified_table(%s)", (table_name,))
        conn.commit()

        print(f"Table '{table_name}' created successfully.\n")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating table: {error}")
    finally:
        if conn is not None:
            conn.close()

def create_simplified_table(simplified_table_name:str, non_simplified_table_name:str)->None:
    try:
        conn = criar_conexao()
        cur = conn.cursor()
        
        # Call the stored procedure function
        cur.execute("SELECT create_simplified_table(%s, %s)", (simplified_table_name, non_simplified_table_name))
        conn.commit()

        print(f"Table '{simplified_table_name}' table created successfully.\n")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating table: {error}")
    finally:
        if conn is not None:
            conn.close()

def calculate_epsilon(canvas_width, canvas_height, points):
    max_distance = 0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        distance = ((y2 - y1)**2 + (x2 - x1)**2)**0.5
        max_distance = max(max_distance, distance)
    return max(canvas_width, canvas_height) * 0.005 * (max_distance / (len(points) - 1)) 

def calculate_canvas_size(points):
    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_y = max(point[1] for point in points)

    canvas_width = max_x - min_x + 20  
    canvas_height = max_y - min_y + 20  

    print("Canvas dimension: ", canvas_width, "x", canvas_height)

    return canvas_width, canvas_height

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

def appFunction(points, canvas_width, canvas_height, executionTime):

    epsilon = calculate_epsilon(canvas_width, canvas_height, points)

    simplified_points = ramer_douglas_peucker(points, epsilon)

    user_input_table_name = input("Enter a name for the non simplified points table: ")

    non_simplified_table_name = "non_simplified_points_path_" + str(executionTime) + "_" + user_input_table_name
    create_non_simplified_table(non_simplified_table_name)
    # modified_string = non_simplified_table_name.replace("non_simplified_points", "")
    create_simplified_table("simplified_points", non_simplified_table_name)

    root = tk.Tk()
    root.title("Simplified Line with Points")

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

   
    draw_line(canvas, points, "black")
    draw_line(canvas, simplified_points, "blue")

   
    root.mainloop()

def runApp():

    executionTime = 1

    while True:
        points = generate_random_points(300)
        canvas_width, canvas_height = calculate_canvas_size(points)
        appFunction(points, canvas_width, canvas_height, str(executionTime))
        user_input_app = input("More data? (y/n): ").strip().lower()
        if user_input_app == 'n':
            break
        else:
            executionTime += 1
            print(f"Execution time incremented to {executionTime}\n")
