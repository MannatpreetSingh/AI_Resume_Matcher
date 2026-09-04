import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    ca_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "ca.pem"
    )

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT", "4000")),
        database=os.getenv("DB_NAME"),
        ssl_ca=ca_path,
        auth_plugin="mysql_native_password"
    )

    return connection