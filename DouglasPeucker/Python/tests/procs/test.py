import psycopg2
from datetime import datetime

# Establish a connection to your PostgreSQL database
conn = psycopg2.connect(
    database="rdp_storage",
    host="localhost",
    user="postgres",
    password="123456",
    port="5432"
)

def create_custom_table(conn, table_name):
    cur = conn.cursor()

    non_simplified_points = "non_simplified_points"

    # Generate the table name based on user input and current datetime
    formatted_table_name = f"{table_name}_{datetime.now().strftime('%d_%m_%y_%H_%M_%S')}"

    # Define the SQL query to create the custom table
    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {non_simplified_points + "_" + formatted_table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            age INT
        );
    """

    # Execute the SQL query to create the custom table
    cur.execute(create_table_sql)
    conn.commit()

    print(f"Custom table '{non_simplified_points + "_" + formatted_table_name}' created successfully!")

    cur.close()

# Example usage: Prompt the user to input a table name
user_input_table_name = input("Enter a name for the non simplified points table: ")

# Call the function to create a custom table with the user-specified name
create_custom_table(conn, user_input_table_name)

# Close the database connection
conn.close()
