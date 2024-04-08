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
points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 0), (6, 1), (7, 2), (8, 3), (9, 4)]
# points = [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 0), (6, 1), (7, 4), (8, 9), (9, 16)]


tolerance = 0.5

simplified_points = douglas_peucker(points, tolerance)
print("Pontos originais:", points)
print("Pontos simplificados:", simplified_points)

# Função para desenhar pontos originais
def desenhar_pontos_originais(canvas, points):
    for point in points:
        x, y = point
        canvas.create_oval(x * 50 + 45, 255 - y * 50, x * 50 + 55, 245 - y * 50, fill="red")

# Função para desenhar pontos simplificados
def desenhar_pontos_simplificados(canvas, simplified_points):
    for point in points:
        x, y = point
        canvas.create_oval(x * 50 + 45, 255 - y * 50, x * 50 + 55, 245 - y * 50, fill="blue")

# Função para desenhar a linha entre os pontos simplificados
def desenhar_linha_entre_pontos_simplificados(canvas, points):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        canvas.create_line(x1 * 50 + 50, 250 - y1 * 50, x2 * 50 + 50, 250 - y2 * 50, fill="blue", width=1)

# Inicializa a janela e o canvas
root = tk.Tk()
root.title("Pontos Originais e Simplificados com Linha")

canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

# Desenha os eixos x e y
canvas.create_line(50, 250, 300, 250, arrow=tk.LAST)  # Eixo x
canvas.create_line(50, 250, 50, 50, arrow=tk.LAST)    # Eixo y

# Desenha os pontos originais em vermelho
desenhar_pontos_originais(canvas, points)

# Desenha os pontos simplificados em azul
desenhar_pontos_simplificados(canvas, simplified_points)

# Desenha a linha entre os pontos simplificados em verde
desenhar_linha_entre_pontos_simplificados(canvas, simplified_points)

# Inicia o loop da interface gráfica
root.mainloop()
