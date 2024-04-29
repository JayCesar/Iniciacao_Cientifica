import BdConfig 

cursor = BdConfig.criar_conexao().cursor()

cursor.execute('select * from pontos')
print(cursor.fetchall())
