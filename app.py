import sqlite3
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort, redirect, render_template, request, session
import config
import db
import reviews
import users
import secrets
import markupsafe

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
def index():
    all_reviews = reviews.get_reviews()
    return render_template("index.html", reviews=all_reviews)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    reviews = users.get_reviews(user_id)
    return render_template("show_user.html", user=user, reviews=reviews)

@app.route("/find_review")
def find_review():
    query = request.args.get("query")
    if query:
        results = reviews.find_reviews(query)
    else:
        query = ""
        results = []
    return render_template("find_review.html", query=query, results=results)

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/review/<int:review_id>")
def show_review(review_id):
    review = reviews.get_review(review_id)
    classes = reviews.get_classes(review_id)
    comments = reviews.get_comment(review_id)
    return render_template("show_review.html", review=review, classes=classes, comments=comments)


@app.route("/new_review")
def new_review():
    require_login()
    classes = reviews.get_all_classes()
    return render_template("new_review.html", classes=classes)


@app.route("/create_review", methods=["POST"])
def create_review():
    require_login()
    check_csrf()
    title = request.form["title"]
    if len(title) > 50:
        abort(403)
    author = request.form["author"]
    year = request.form["year"]
    description = request.form["description"]
    if len(description) > 1000:
        abort(403)
    user_id = session["user_id"]

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            classes.append((parts[0],parts[1]))
    reviews.add_review(title, author, year, description, user_id, classes)
    return redirect("/")

@app.route("/new_comment", methods=["POST"])
def new_comment():
    require_login()
    check_csrf()
    review_id = request.form["review_id"]
    user_id = session["user_id"]
    comment = request.form["comment"]
    review = reviews.get_review(review_id)


    reviews.add_comment(review_id, user_id, comment)

    return redirect("/review/" + str(review_id))

@app.route("/edit_review/<int:review_id>")
def edit_review(review_id):
    require_login()
    review = reviews.get_review(review_id)
    if review["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_review.html", review=review)


@app.route("/update_review", methods=["POST"])
def update_review_route():
    require_login()
    check_csrf()
    required_fields = ["review_id", "title", "author", "year", "description"]
    missing_fields = [key for key in required_fields if key not in request.form]

    if missing_fields:
        return "Bad Request: Missing fields", 400

    review_id = request.form["review_id"]
    review = reviews.get_review(review_id)

    if review["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    author = request.form["author"]
    year = request.form["year"]
    description = request.form["description"]

    genre = review.get("genre", None)
    stars = review.get("stars", None)

    print(f"Updating review {review_id}: title={title}, author={author}, year={year}, description={description}, genre={genre}, stars={stars}")

    reviews.update_review(review_id, title, author, year, description)

    return redirect("/review/" + str(review_id))


@app.route("/remove_review/<int:review_id>", methods=["GET", "POST"])
def remove_review(review_id):
    require_login()
    review = reviews.get_review(review_id)
    if review["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_review.html", review=review)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            reviews.remove_comments(review_id)
            reviews.remove_review_classes(review_id)
            reviews.remove_review(review_id)
            return redirect("/")

        else:
            return redirect("/review/" + str(review_id))


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session["csrf_token"] = secrets.token_hex(16)
        return render_template("login.html")
    if request.method == "POST":
        check_csrf()
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")