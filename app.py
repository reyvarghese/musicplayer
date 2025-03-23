import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="musicplayer",
        user="myuser",
        password="mypassword",
        host="localhost",  # or use 'db' if running inside Docker Compose
        port="5432"
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Connect to database and insert user
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cur.close()
        conn.close()

        return f"Welcome, {username}!"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)

