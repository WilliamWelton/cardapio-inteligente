from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Rota para visualizar pedidos
@app.route('/ver_pedidos')
def ver_pedidos():
    try:
        # Conectar ao banco de dados MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="will",  # Substitua pelo seu usuário MySQL
            password="Acai123@#",  # Substitua pela sua senha MySQL
            database="banco_acai"  # Substitua pelo nome do seu banco de dados
        )
        cursor = conn.cursor()

        # Consulta SQL para buscar os pedidos
        cursor.execute("SELECT cliente_nome, tamanho, fruta, adicionais, calda, pagamento, hora_pedido FROM pedidos")
        pedidos = cursor.fetchall()

        # Fechar a conexão
        cursor.close()
        conn.close()

        # Renderizar os dados na página HTML
        return render_template('ver_pedidos.html', pedidos=pedidos)

    except mysql.connector.Error as err:
        return f"Erro ao conectar ao banco de dados: {err}"

if __name__ == '__main__':
    app.run(debug=True)
