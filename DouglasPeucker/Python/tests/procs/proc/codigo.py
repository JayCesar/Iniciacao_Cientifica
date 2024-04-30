import psycopg2

def criar_conexao():
    try:
        # Estabelece a conexão com o banco de dados PostgreSQL
        conexao = psycopg2.connect(database="rdp_storage",
                                   host="localhost",
                                   user="postgres",
                                   password="123456",
                                   port="5432")
        print("Conexão PostgreSQL estabelecida com sucesso.\n")
        return conexao  # Retorna a conexão estabelecida

    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados PostgreSQL:", e)
        return None  # Retorna None se a conexão falhar


def create_non_simplified_table(table_name):
    try:
        conn = criar_conexao()
        cur = conn.cursor()

        # Call the stored procedure function
        cur.execute("SELECT create_non_simplified_table(%s)", (table_name,))
        conn.commit()

        print(f"Table '{table_name}' created successfully.\n")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating table: {error}")
    finally:
        if conn is not None:
            conn.close()

def create_simplified_table(simplified_table_name:str, non_simplified_table_name:str)->None:
    try:
        conn = criar_conexao()
        cur = conn.cursor()
        
        # Call the stored procedure function
        cur.execute("SELECT create_simplified_table(%s, %s)", (simplified_table_name, non_simplified_table_name))
        conn.commit()

        print(f"Table '{simplified_table_name}' created successfully.\n")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating table: {error}")
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    try:
       
        simplified_table_name = "my_simplified_table"
        non_simplified_table_name = "my_non_simplified_table"

        # Call the procedure function to create the simplified table
        create_non_simplified_table(non_simplified_table_name)
        create_simplified_table(simplified_table_name, non_simplified_table_name)
    

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
   