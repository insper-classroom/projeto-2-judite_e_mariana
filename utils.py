from select import select
import os
import mysql

def conect_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        ca_pem="projeto-2-judite_e_mariana/ca.pem"
    )
    