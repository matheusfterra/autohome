import pymysql

# Abrimos uma conexão com o banco de dados:
conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')

# Cria um cursor:
cursor = conexao.cursor()
