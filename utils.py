from select import select
import os
import mysql.connector

def conect_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        ssl_ca="projeto-2-judite_e_mariana/ca.pem"
    )

def list_imoveis():
    conn = conect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis")
    rows = cursor.fetchall()
    
    colunas = [desc[0] for desc in cursor.description]
    imoveis = [dict(zip(colunas, row)) for row in rows]
    
    conn.close()
    return imoveis
