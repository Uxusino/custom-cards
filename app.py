import os
import sys
from flask import Flask
from flask import render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users/<string:username>")
def user(username):
    return render_template("profile.html", username=username)

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        res = db.session.execute(text("SELECT username FROM users"))
        users = res.fetchall()
        users = [u[0] for u in users]
        print(users, file=sys.stderr)
        if username in users:
            flash("This username already exists.", "error")
            return render_template("register.html")
        profile_url = "/users/" + username
        return redirect(profile_url)
    return render_template("register.html")

@app.route("/simulator")
def simulator():
    return "This page will contain simulation of CAH, where you can test your cards."