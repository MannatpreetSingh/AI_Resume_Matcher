from flask import Flask, render_template, request, redirect, url_for, session
from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from utils.matcher import calculate_match
from utils.ai_matcher import caluclate_similarity


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def home():
    return "AI Resume & Job-Fit Matcher is running!"


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (name, email, hashed_password))

        connection.commit()

        cursor.close()
        connection.close()

        return "Registration successful!"

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE email = %s"

        cursor.execute(query, (email,))

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect(url_for("dashboard"))

        return "Invalid email or password!"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT *
    FROM results
    WHERE user_id = %s
    ORDER BY created_at DESC
    """

    cursor.execute(query, (session["user_id"],))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
    "dashboard.html",
    name=session["user_name"],
    results=results
)


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        file = request.files["resume"]
        job_description = request.form["job_description"]

        if file.filename == "":
            return "No file selected"

        if not file.filename.lower().endswith(".pdf"):
            return "Only PDF files are supported"

        filename = file.filename

        upload_folder = "uploads"

        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)

        file.save(file_path)

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

            
            skill_result = calculate_match(
                text,
                job_description
            )

           
            similarity = caluclate_similarity(
                text,
                job_description
            )

         
            matched_count = len(skill_result["matched_skills"])
            missing_count = len(skill_result["missing_skills"])

            total_skills = matched_count + missing_count

            
            if total_skills > 0:

                skill_percentage = (
                    matched_count / total_skills
                ) * 100

            else:

                skill_percentage = 0

                
            if skill_percentage == 100:
                final_score = 100
            else:
                final_score = (
                skill_percentage * 0.80
                + similarity * 0.20
            )

                
            result = {

                    "match_percentage": round(final_score, 2),

                    "matched_skills": skill_result["matched_skills"],

                    "missing_skills": skill_result["missing_skills"]
                }

                
            connection = get_db_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO results(
                    user_id,
                    job_description,
                    match_percentage,
                    matched_skills,
                    missing_skills
                )
                VALUES(%s, %s, %s, %s, %s)
                """

            cursor.execute(
                    query,
                    (
                        session["user_id"],
                        job_description,
                        result["match_percentage"],
                        ", ".join(result["matched_skills"]),
                        ", ".join(result["missing_skills"])
                    )
                )

            connection.commit()

            cursor.close()
            connection.close()

        return render_template(
            "result.html",
            result=result
        )

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
