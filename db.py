import mysql.connector
import os

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT", 4000)),
        database=os.getenv("DB_NAME"),
        ssl_ca=os.getenv("DB_SSL_CA")
    )
    return connection