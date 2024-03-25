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
# points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
# points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 0), (6, 1), (7, 2), (8, 3), (9, 4)]
points = [(0, 0), (0.5, 0.5), (1, 1), (1.5, 1.5), (2, 2), (2.5, 2.5), (3, 3), (3.5, 3.5), (4, 4)]


tolerance = 0.2

simplified_points = douglas_peucker(points, tolerance)
print("Pontos originais:", points)
print("Pontos simplificados:", simplified_points)

# Filtra os pontos para manter apenas os pontos com coordenadas positivas
positive_points = [point for point in simplified_points if point[0] >= 0 and point[1] >= 0]

# Ajusta a escala dos pontos considerando apenas a parte positiva dos eixos x e y
scaled_points = [(point[0], point[1]) for point in positive_points]

# Função para desenhar linhas com base nos pontos
def desenhar_linhas(canvas, points, color):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        canvas.create_line(x1 * 50 + 50, 250 - y1 * 50, x2 * 50 + 50, 250 - y2 * 50, fill=color)

# Inicializa a janela e o canvas
root = tk.Tk()
root.title("Linhas Simplificadas")

canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

# Desenha os eixos x e y
canvas.create_line(50, 250, 300, 250, arrow=tk.LAST)  # Eixo x
canvas.create_line(50, 250, 50, 50, arrow=tk.LAST)    # Eixo y

# Desenha as linhas simplificadas no gráfico
desenhar_linhas(canvas, scaled_points, "blue")

# Inicia o loop da interface gráfica
root.mainloop()
