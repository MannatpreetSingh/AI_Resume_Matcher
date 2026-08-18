import mysql.connector

def get_db_connection():
    connection=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3307,
        database="resume_matcher"
    )
    return connection
