import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('reconhecimento.db')
c = conn.cursor()

# Executar a instrução SQL para excluir todas as linhas da tabela "registros"
c.execute("DELETE FROM registros")

# Confirmar as alterações no banco de dados
conn.commit()

# Fechar a conexão com o banco de dados
conn.close()
