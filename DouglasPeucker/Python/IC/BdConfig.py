import psycopg2

def criar_conexao():
    try:
        # Estabelece a conexão com o banco de dados PostgreSQL
        conexao = psycopg2.connect(database="rdp_storage",
                                   host="localhost",
                                   user="postgres",
                                   password="123456",
                                   port="5432")
        print("Conexão PostgreSQL estabelecida com sucesso.")
        return conexao  # Retorna a conexão estabelecida

    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados PostgreSQL:", e)
        return None  # Retorna None se a conexão falhar


