from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuração do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'will',
    'password': 'Acai123@#',
    'database': 'banco_acai'
}

def salvar_pedido(cliente_nome, tamanho, fruta, adicionais, calda, pagamento):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Inserir dados na tabela
    cursor.execute("""
    INSERT INTO pedidos (cliente_nome, tamanho, fruta, adicionais, calda, pagamento)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (cliente_nome, tamanho, fruta, ','.join(adicionais), calda, pagamento))

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cliente_nome = request.form.get('nome')
        tamanho = request.form.get('tamanho')
        fruta = request.form.get('fruta')
        adicionais = request.form.getlist('adicionais')
        calda = request.form.get('calda')
        pagamento = request.form.get('pagamento')

        # Map valores para nomes de arquivos de imagens
        nome_tamanho = f"{tamanho}.jpg"
        nome_fruta = f"{fruta}.jpg"
        nome_calda = f"calda_{calda.replace(' ', '_')}.jpg"
        adicionais_imagens = [f"{adicional.replace(' ', '_')}.jpg" for adicional in adicionais]

        # Salvar pedido no banco de dados
        salvar_pedido(cliente_nome, nome_tamanho, nome_fruta, adicionais_imagens, nome_calda, pagamento)

        return redirect(url_for('recebimento', nome=cliente_nome, tamanho=nome_tamanho, fruta=nome_fruta, adicionais=','.join(adicionais_imagens), calda=nome_calda, pagamento=pagamento))

    return render_template('pedido.html')

@app.route('/recebimento')
def recebimento():
    cliente_nome = request.args.get('nome')
    tamanho = request.args.get('tamanho')
    fruta = request.args.get('fruta')
    adicionais = request.args.get('adicionais').split(',')  # Separar a lista de adicionais
    calda = request.args.get('calda')
    pagamento = request.args.get('pagamento')

    # Corrigir o caminho dos arquivos se necessário
    adicionais = [adicional for adicional in adicionais if adicional]  # Remover entradas vazias

    return render_template('recebimento.html', nome=cliente_nome, nome_tamanho=tamanho, nome_fruta=fruta, adicionais=adicionais, nome_calda=calda, pagamento=pagamento)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/ver_pedidos')
def ver_pedidos():
    connection = mysql.connector.connect(
        host='localhost',
        user='will',
        password='Acai123@#',
        database='acai_pedidos'
    )

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pedidos ORDER BY hora_pedido")
    pedidos = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('ver_pedidos.html', pedidos=pedidos)
