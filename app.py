from flask import Flask , render_template, request
from db import get_db_connection
from werkzeug.security import generate_password_hash
app=Flask(__name__)


@app.route("/")
def home():
    return "AI Resume & Job-Fit Matcher is running!"
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        name=request.form["name"]
        email=request.form["email"]
        password = request.form["password"]
        
        hashed_password= generate_password_hash(password)
        connection=get_db_connection()
        cursor= connection.cursor()
        
        query="""
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (name, email, hashed_password))
        connection.commit()
        cursor.close()
        connection.close()
        return "Registration successful!"
    return render_template("register.html")

if __name__== "__main__":
     app.run(debug=True)
     
