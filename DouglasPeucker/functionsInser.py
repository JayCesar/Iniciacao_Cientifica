def insert_non_simplified_points(conn, points, table_name, executionTime):
    cur = conn.cursor()

    # Construct the non-simplified table name
    non_simplified_table_name = f"non_simplified_points_path_{executionTime}_{table_name}"

    # Create the non-simplified points table if it doesn't exist
    create_non_simplified_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {non_simplified_table_name} (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255),
            ponto geometry(Point, 4326)
        );
    """
    cur.execute(create_non_simplified_table_sql)
    conn.commit()

    # Insert points into the non-simplified points table
    for point in points:
        x, y = point
        insert_point_sql = f"INSERT INTO {non_simplified_table_name} (nome, ponto) VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))"
        data = (f"Point ({x}, {y})", x, y)
        cur.execute(insert_point_sql, data)
    conn.commit()

    cur.close()

    print(points)

    return non_simplified_table_name

def insert_simplified_points(conn, simplified_points, non_simplified_table_name, non_simplified_id):
    cur = conn.cursor()

    result_string = non_simplified_table_name.replace("non_simplified_points_", "")

    # Construct the simplified points table name
    simplified_table_name = f"simplified_points_{result_string}"

    # Create the simplified points table if it doesn't exist
    create_simplified_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {simplified_table_name} (
            id SERIAL PRIMARY KEY,
            simplified_nome VARCHAR(255),
            simplified_ponto geometry(Point, 4326),
            non_simplified_id INT REFERENCES {non_simplified_table_name}(id)
        );
    """
    cur.execute(create_simplified_table_sql)
    conn.commit()

    # Insert simplified points into the simplified points table
    for point in simplified_points:
        x, y = point
        insert_simplified_point_sql = f"INSERT INTO {simplified_table_name} (simplified_nome, simplified_ponto, non_simplified_id) VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s)"
        data = (f"Simplified Point ({x}, {y})", x, y, non_simplified_id)
        cur.execute(insert_simplified_point_sql, data)
    conn.commit()

    cur.close()

    print(simplified_points)

    return simplified_table_name