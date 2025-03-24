from flask import Flask, request, render_template, redirect, url_for, flash
import psycopg2
import hashlib

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flashing messages

# Database connection
try:
    conn = psycopg2.connect(
        dbname="musicplayer",
        user="myuser",
        password="mypassword",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    print("✅ Successfully connected to the 'musicplayer' database!")
except Exception as e:
    print("❌ Failed to connect to the database:", e)

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("Password123".encode()).hexdigest()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if username == ADMIN_USERNAME and hashed_password == ADMIN_PASSWORD_HASH:
            flash("✅ Login Successful!", "success")
        else:
            flash("❌ Access Denied. Only the admin can log in.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
