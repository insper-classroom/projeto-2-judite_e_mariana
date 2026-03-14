from select import select
import os
import mysql.connector

# função para conectar ao banco de dados
def conect_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        ssl_ca="projeto-2-judite_e_mariana/ca.pem"
    )

def list_imoveis():
    #conecta ao db
    conn = conect_db()
    cursor = conn.cursor()
    
    #seleciona os imoveis do banco de dados
    cursor.execute("SELECT * FROM imoveis")
    rows = cursor.fetchall()
    
    #formata como dicionario a lista de imoveis
    colunas = [desc[0] for desc in cursor.description]
    imoveis = [dict(zip(colunas, row)) for row in rows]
    
    conn.close()
    return imoveis
