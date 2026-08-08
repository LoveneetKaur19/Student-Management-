from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app import app
from models import db, User


# =====================================
# HOME
# =====================================

@app.route("/")
def home():
    return render_template("home.html")


# =====================================
# SIGNUP
# =====================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        existing = User.query.filter_by(email=email).first()

        if existing:
            flash("Email already registered!", "danger")
            return redirect("/signup")

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        flash("Account Created Successfully!", "success")
        return redirect("/login")

    return render_template("signup.html")


# =====================================
# LOGIN
# =====================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Invalid Email", "danger")
            return redirect("/login")

        if not check_password_hash(user.password, password):
            flash("Invalid Password", "danger")
            return redirect("/login")

        session["user_id"] = user.id
        session["username"] = user.username

        flash("Login Successful!", "success")
        return redirect("/dashboard")

    return render_template("login.html")


# =====================================
# LOGOUT
# =====================================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully!", "success")
    return redirect("/login")