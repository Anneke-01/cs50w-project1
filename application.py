import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for, flash,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions

from helpers import login_required

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        # if session.get("user_id") is None:
        # return redirect("/login")
        if not request.form.get("book"):
            return render_template("error.html", message="You must submit book info.")
        search = "%" + request.form.get("book") +"%"
        search = search.title()
        books = db.execute(
            "SELECT isbn, title, author, year FROM books where isbn LIKE :search OR title LIKE :search OR author LIKE :search OR year LIKE :search")
        if len(books) == 0:
            return render_template("error.html", message="No matching results.")
        else:
            return render_template("results.html", books=books)
    else:
        return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        ##if session.get("user_id") is None:
        ##    return redirect("/login")  
        if not request.form.get("book"):
            return render_template("error.html", message="You must submit book info.")
        search = request.form.get("book").lower()
        book = "%" + search + "%"
        books = db.execute(
            "SELECT * FROM books WHERE (LOWER(isbn) LIKE :book) OR (LOWER(title) LIKE :book) OR (LOWER(author) LIKE :book) LIMIT 15", {"book": book}).fetchall()
        if len(books) == 0:
            return render_template("error.html", message="No results :(")
        else:
            return render_template("results.html", search=search, books=books)
    else:
        return render_template("index.html")

@app.route("/book/<isbn>", methods=["GET", "POST"])
@login_required
def book(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return "Error"
    return render_template("book.html", book=book)

@app.route("/review", methods=["GET", "POST"])
@login_required
def review():
    return render_template("review.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        respuesta = db.execute("SELECT id FROM users WHERE username = :username OR email = :email", {
                               "username": username, "email": email}).fetchall()
        if len(respuesta) != 0:
            return render_template("error.html", message="Username taken.")

        password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users(username,email, password) VALUES(:username,:email, :password)",
                    {"username": username, "email": email, "password": password})
        db.commit()
        
        ## crasheaaaaaaaaaaaaaaaaaaaaaaaaaa
        session["user_id"] = respuesta
        flash("Registered!")
        return redirect(url_for("index"))
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
       
        if not username:
            return "must provide username",403

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "must provide password", 403
        print(username)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          {"username": username}).fetchall()

        print(rows)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return render_template("error.html", message="invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect(url_for("index"))
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    # Redirect user to login form
    return redirect(url_for("index"))

@app.route("/api/<isbn>")
def api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn": isbn}).fetchone()

    if book is None:
        return "invalid ISBN number"
    else:
        response = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+isbn).json()

        data = response['items'][0]['volumeInfo']
        promedio = data["averageRating"]
        ratings = data["ratingsCount"]
        api = jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": ratings,
            "average_score": promedio
        })
        return api




if __name__ == '__main__':
    app.run(port=3300)

