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
    denominator = ((y2 - y1)**2 + (x2 - x1)**2)**0.5
    
    return nominator / denominator

# Exemplo de uso
points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (200, 100), (6, 0), (7, 0), (8, 8), (200, 390)]
tolerance = 0.5

simplified_points = douglas_peucker(points, tolerance)
print("Pontos originais:", points)
print("Pontos simplificados:", simplified_points)

# Inicializa a janela e o canvas
root = tk.Tk()
root.title("Pontos Simplificados")

canvas_width = 400
canvas_height = 400

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Desenha os pontos simplificados em azul
for point in simplified_points:
    x, y = point
    canvas.create_oval(x - 2, canvas_height - y - 2, x + 2, canvas_height - y + 2, fill="blue")

# Inicia o loop da interface gráfica
root.mainloop()
