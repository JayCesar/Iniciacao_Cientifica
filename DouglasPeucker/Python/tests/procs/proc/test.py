import psycopg2
from random import randint

# Establish a connection to your PostgreSQL database
conn = psycopg2.connect(
    database="rdp_storage",
    host="localhost",
    user="postgres",
    password="123456",
    port="5432"
)

def format_point_data(points):
    # Construct a PostgreSQL array string representation of points
    return "{" + ",".join(f"'POINT({point[0]} {point[1]})'" for point in points) + "}"

def invoke_insert_non_simplified_points(points, table_name):
    cur = conn.cursor()
    points_data = format_point_data(points)
    # Construct the SQL query to call the PostgreSQL function with the array parameter
    sql_query = f"CALL insert_non_simplified_points(ARRAY{points_data}::geometry[], %s)"
    cur.execute(sql_query, (table_name,))
    conn.commit()
    cur.close()

def invoke_insert_simplified_points(simplified_points, non_simplified_table_name, non_simplified_id):
    cur = conn.cursor()
    simplified_points_data = format_point_data(simplified_points)
    # Construct the SQL query to call the PostgreSQL function with the array parameter
    sql_query = f"CALL insert_simplified_points(ARRAY{simplified_points_data}::geometry[], %s, %s)"
    cur.execute(sql_query, (non_simplified_table_name, non_simplified_id))
    conn.commit()
    cur.close()

# Example usage:
points = [(randint(0, 300), randint(0, 300)) for _ in range(10)]  # Generate random points
table_name = "example_table"

invoke_insert_non_simplified_points(points, table_name)

# Retrieve the ID of the last inserted non-simplified point
cur = conn.cursor()
cur.execute(f"SELECT MAX(id) FROM non_simplified_points_path_{table_name}")
non_simplified_id = cur.fetchone()[0]
cur.close()

# Close the database connection at the end
conn.close()
