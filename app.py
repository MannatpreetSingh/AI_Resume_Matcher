from flask import Flask
from db import get_db_connection

app=Flask(__name__)


@app.route("/")
def home():
    connection = get_db_connection()
    if connection.is_connected():
        connection.close()
        return "Flask + mysql connected successfully "


if __name__== "__main__":
     app.run(debug=True)
     
