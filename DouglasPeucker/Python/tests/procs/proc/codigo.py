import psycopg2

# Establish a connection to your PostgreSQL database
conn = psycopg2.connect(
    database="rdp_storage",
    host="localhost",
    user="postgres",
    password="123456",
    port="5432"
)

def call_insert_non_simplified_points(conn, points, table_name):
    cur = conn.cursor()
    try:
        cur.callproc("insert_non_simplified_points", (points, table_name,))
        conn.commit()
        print("Stored procedure insert_non_simplified_points executed successfully.")
    except psycopg2.Error as e:
        print(f"Error calling stored procedure insert_non_simplified_points: {e}")
    finally:
        cur.close()

def call_insert_simplified_points(conn, simplified_points, non_simplified_id, table_name):
    cur = conn.cursor()
    try:
        cur.callproc("insert_simplified_points", (simplified_points, non_simplified_id, table_name,))
        conn.commit()
        print("Stored procedure insert_simplified_points executed successfully.")
    except psycopg2.Error as e:
        print(f"Error calling stored procedure insert_simplified_points: {e}")
    finally:
        cur.close()

# Example usage:
points = [(10.0, 20.0), (30.0, 40.0), (50.0, 60.0)]  # Example non-simplified points
simplified_points = [(15.0, 25.0), (35.0, 45.0)]     # Example simplified points

# Prompt user to enter a custom table name
table_name = input("Enter a name for the table: ")

# Call the stored procedures with the custom table name
call_insert_non_simplified_points(conn, points, table_name)
call_insert_simplified_points(conn, simplified_points, 1, table_name)  # Assuming non_simplified_id is 1

# Close the database connection at the end
conn.close()
