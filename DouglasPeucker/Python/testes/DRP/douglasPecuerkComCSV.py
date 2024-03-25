import csv

def douglas_peucker(points, tolerance):
    if len(points) <= 2:
        return points
    
    max_distance = 0
    index = 0
    end = len(points) - 1
    
    for i in range(1, end):
        distance = perpendicular_distance(points[i], points[0], points[end])
        if distance > max_distance:
            index = i
            max_distance = distance
    
    if max_distance > tolerance:
        left_part = douglas_peucker(points[:index + 1], tolerance)
        right_part = douglas_peucker(points[index:], tolerance)
        
        return left_part[:-1] + right_part
    else:
        return [points[0], points[end]]

def perpendicular_distance(point, line_start, line_end):
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

nome_arquivo_csv = "pontos_simplificados.csv"

with open(nome_arquivo_csv, 'w', newline='') as arquivo_csv:

    escritor_csv = csv.writer(arquivo_csv)

    escritor_csv.writerow(["X", "Y"])
    for ponto in simplified_points:
        escritor_csv.writerow( ponto )

print(f'Pontos simplificados foram salvos no arquivo {nome_arquivo_csv}')
