from flask import Flask, request, redirect
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


# Carrega as variáveis de ambiente do arquivo .cred (se disponível)
load_dotenv('.cred')

# Configurações para conexão com o banco de dados usando variáveis de ambiente
config = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
    'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
    'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
    'database': os.getenv('DB_NAME', 'db_escola'),  # Obtém o nome do banco de dados da variável de ambiente
    'port': int(os.getenv('DB_PORT', 3306)),  # Obtém a porta do banco de dados da variável de ambiente
    'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
}


# Função para conectar ao banco de dados
def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None
    
app = Flask(__name__)

@app.route('/imoveis', methods=['GET'])
def get_imoveis():
    #conecta ao db
    conn = connect_db()
    
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500
    
    cursor = conn.cursor()
    
    #seleciona os imoveis do banco de dados
    cursor.execute("SELECT * FROM imoveis")
    
    results = cursor.fetchall()
    if not results:
        resp = {"erro": "Nenhum imovel encontrado"}
        return resp, 404
    else:
        imoveis = []
        for imovel in results:
            dic_imovel = {
                'id': imovel[0],
                'logradouro': imovel[1],
                'tipo_logradouro': imovel[2],
                'bairro': imovel[3],
                'cidade': imovel[4],
                'cep': imovel[5],
                'tipo': imovel[6],
                'valor': float(imovel[7]),
                'data_aquisicao': str(imovel[8])
            }
            imoveis.append(dic_imovel)
    
    conn.close()
    return {"imoveis": imoveis}, 200


@app.route('/imoveis/<int:id>', methods=['GET'])
def get_imovel_por_id(id):
    # conectar com a base de dados
    conn = connect_db()

    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
    result = cursor.fetchone()

    if result is None:
        resp = {"erro": "Imóvel não encontrado"}
        return resp, 404
    else:
        imovel = {
            'id': result[0],
            'logradouro': result[1],
            'tipo_logradouro': result[2],
            'bairro': result[3],
            'cidade': result[4],
            'cep': result[5],
            'tipo': result[6],
            'valor': float(result[7]),
            'data_aquisicao': str(result[8])
        }

    conn.close()
    return imovel, 200


@app.route('/submit', methods=['POST'])
def new_imovel():
    # verifica se os dados estão incompletos antes de acessar o banco de dados
    if not request.json or request.json.get('logradouro') == '' or request.json.get('tipo_logradouro') == '' or request.json.get('bairro') == '' or request.json.get('cidade') == '' or request.json.get('cep') == '' or request.json.get('tipo') == '' or request.json.get('valor') == '' or request.json.get('data_aquisicao') == '':
        return {"erro": "Dados incompletos"}, 400
    
    #conecta ao db
    conn = connect_db()
    
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (request.json['logradouro'], request.json['tipo_logradouro'], request.json['bairro'], request.json['cidade'], request.json['cep'], request.json['tipo'], request.json['valor'], request.json['data_aquisicao']))
    
    if request.json['logradouro'] == '' or request.json['tipo_logradouro'] == '' or request.json['bairro'] == '' or request.json['cidade'] == '' or request.json['cep'] == '' or request.json['tipo'] == '' or request.json['valor'] == '' or request.json['data_aquisicao'] == '':
        return {"erro": "Dados incompletos"}, 400
    
    conn.commit()
    conn.close()
    return {"mensagem": "Imóvel cadastrado com sucesso"}, 200



if __name__ == '__main__':
    app.run(debug=True)