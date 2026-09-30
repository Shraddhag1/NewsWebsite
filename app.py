from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = "newswave_secret_key"

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "newswave.db")


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    # Add sample news only if database is empty
    count = conn.execute("SELECT COUNT(*) FROM news").fetchone()[0]

    if count == 0:
        sample_news = [
            (
                "Technology is Changing the World",
                "New technologies are changing the way people work and communicate.",
                "Technology"
            ),
            (
                "Business Market Updates",
                "The business sector continues to experience major changes.",
                "Business"
            ),
            (
                "Latest Sports News",
                "Get the latest updates from the world of sports.",
                "Sports"
            ),
            (
                "Important Political Updates",
                "Read the latest political news and developments.",
                "Politics"
            )
        ]

        conn.executemany(
            "INSERT INTO news (title, description, category) VALUES (?, ?, ?)",
            sample_news
        )

        conn.commit()

    conn.close()


# ---------------- ADMIN LOGIN ----------------

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("login"))
        return function(*args, **kwargs)

    return wrapper


# ---------------- HOME ----------------

@app.route("/")
def home():

    conn = get_db()

    news = conn.execute(
        "SELECT * FROM news ORDER BY created_at DESC"
    ).fetchall()

    conn.close()

    return render_template("home.html", news=news)


# ---------------- ABOUT ----------------

@app.route("/about")
def about():
    return render_template("about.html")


# ---------------- CONTACT ----------------

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        conn = get_db()

        conn.execute(
            """
            INSERT INTO messages
            (name, email, subject, message)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, subject, message)
        )

        conn.commit()
        conn.close()

        flash("Your message has been sent successfully!")

        return redirect(url_for("contact"))

    return render_template("contact.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin"] = username

            return redirect(url_for("admin"))

        else:

            flash("Invalid username or password.")

    return render_template("login.html")


# ---------------- ADMIN DASHBOARD ----------------

@app.route("/admin")
@login_required
def admin():

    conn = get_db()

    news = conn.execute(
        "SELECT * FROM news ORDER BY created_at DESC"
    ).fetchall()

    messages = conn.execute(
        "SELECT * FROM messages ORDER BY created_at DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        news=news,
        messages=messages
    )


# ---------------- ADD NEWS ----------------

@app.route("/admin/add", methods=["GET", "POST"])
@login_required
def add_news():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        category = request.form["category"]

        conn = get_db()

        conn.execute(
            """
            INSERT INTO news
            (title, description, category)
            VALUES (?, ?, ?)
            """,
            (title, description, category)
        )

        conn.commit()
        conn.close()

        flash("News added successfully!")

        return redirect(url_for("admin"))

    return render_template("add_news.html")


# ---------------- EDIT NEWS ----------------

@app.route("/admin/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_news(id):

    conn = get_db()

    news = conn.execute(
        "SELECT * FROM news WHERE id = ?",
        (id,)
    ).fetchone()

    if news is None:
        conn.close()
        return "News not found"

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        category = request.form["category"]

        conn.execute(
            """
            UPDATE news
            SET title = ?, description = ?, category = ?
            WHERE id = ?
            """,
            (title, description, category, id)
        )

        conn.commit()
        conn.close()

        flash("News updated successfully!")

        return redirect(url_for("admin"))

    conn.close()

    return render_template(
        "edit_news.html",
        news=news
    )


# ---------------- DELETE NEWS ----------------

@app.route("/admin/delete/<int:id>")
@login_required
def delete_news(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM news WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("News deleted successfully!")

    return redirect(url_for("admin"))


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect(url_for("home"))


# ---------------- RUN ----------------

if __name__ == "__main__":

    init_db()

    app.run(debug=True)