import psycopg2

conexao = psycopg2.connect(database = "teste2",
                           host = "localhost",
                           user = "postgres",
                           password = "123456",
                           port = "5432")

print(conexao.info)
print(conexao.status)

cursor = conexao.cursor() # a partir deele consigo fazer consultas
# cursor.execute('select * from pontos')
# print(cursor.fetchall()) # aqui ele mostra o resultado

cursor.execute('select * from pontos2_xy')
print(cursor.fetchall())