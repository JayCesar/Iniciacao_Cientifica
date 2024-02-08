import csv

def douglas_peucker(points, tolerance):
    if len(points) <= 2:
        return points
    
    # Encontrar o ponto com a maior distância
    max_distance = 0
    index = 0
    end = len(points) - 1
    
    for i in range(1, end):
        distance = perpendicular_distance(points[i], points[0], points[end])
        if distance > max_distance:
            index = i
            max_distance = distance
    
    # Verificar se a maior distância está além da tolerância
    if max_distance > tolerance:
        # Recursivamente simplificar os segmentos à esquerda e à direita do ponto encontrado
        left_part = douglas_peucker(points[:index + 1], tolerance)
        right_part = douglas_peucker(points[index:], tolerance)
        
        # Combinar os resultados
        return left_part[:-1] + right_part
    else:
        # Retornar os pontos extremos se a maior distância estiver dentro da tolerância
        return [points[0], points[end]]

def perpendicular_distance(point, line_start, line_end):
    # Calcular a distância perpendicular de um ponto a uma linha definida por dois pontos
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

# Nome do arquivo CSV
nome_arquivo_csv = "pontos_simplificados.csv"

# Abrir o arquivo CSV em modo de escrita
with open(nome_arquivo_csv, 'w', newline='') as arquivo_csv:
    # Criar um objeto escritor CSV
    escritor_csv = csv.writer(arquivo_csv)

    # Escrever os pontos simplificados no arquivo
    escritor_csv.writerow(["X", "Y"])  # Cabeçalho do CSV
    for ponto in simplified_points:
        escritor_csv.writerow( ponto )

print(f'Pontos simplificados foram salvos no arquivo {nome_arquivo_csv}')
