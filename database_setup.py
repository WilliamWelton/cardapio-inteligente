import mysql.connector

# Configuração do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'will',
    'password': 'Acai123@#'
}

# Conectando ao MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Criar o banco de dados se não existir
cursor.execute("CREATE DATABASE IF NOT EXISTS cardapio_db")

# Selecionar o banco de dados
cursor.execute("USE cardapio_db")

# Criar a tabela de pedidos se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_nome VARCHAR(255) NOT NULL,
    tamanho VARCHAR(50),
    fruta VARCHAR(50),
    adicionais TEXT,
    calda VARCHAR(50),
    pagamento VARCHAR(50),
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Fechar a conexão
cursor.close()
conn.close()

print("Banco de dados e tabela criados com sucesso!")
