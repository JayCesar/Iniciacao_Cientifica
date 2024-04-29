import Service as ServiceFunctions
import BdConfig

conn = BdConfig.criar_conexao()

points = ServiceFunctions.generate_random_points(100)

# Calculate canvas size dynamically
canvas_width, canvas_height = ServiceFunctions.calculate_canvas_size(points)

ServiceFunctions.appFunction(points, canvas_width, canvas_height, conn)
