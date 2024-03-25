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
points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
tolerance = 0.5

simplified_points = douglas_peucker(points, tolerance)
print("Pontos originais:", points)
print("Pontos simplificados:", simplified_points)

# Função para desenhar linhas com base nos pontos
def desenhar_linhas(canvas, points, color):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        canvas.create_line(x1 * 50 + 200, 250 - y1 * 50, x2 * 50 + 200, 250 - y2 * 50, fill=color)

# Inicializa a janela e o canvas
root = tk.Tk()
root.title("Linhas Simplificadas")

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Desenha as linhas simplificadas em azul
desenhar_linhas(canvas, simplified_points, "red")

# Inicia o loop da interface gráfica
root.mainloop()
