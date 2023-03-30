from app import app
from flask import render_template, request, redirect, flash, session

import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users/<string:username>")
def user(username):
    userid = users.get_userid(username)
    return render_template("profile.html", username=username, user=userid, current_user=session["username"])

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    login = users.login(username, password)
    success = login[0]
    if not success:
        error_msg = login[1]
        flash(error_msg)
        return redirect("/")
    else:
        session["username"] = username
        return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        new_user = users.new_user(username, password)
        succes = new_user[0]
        if not succes:
            error_msg = new_user[1]
            flash(error_msg)
            return render_template("register.html")
        else:
            session["username"] = username
            profile_url = "/users/" + username
            return redirect(profile_url)
    return render_template("register.html")

@app.route("/simulator")
def simulator():
    return "This page will contain simulation of CAH, where you can test your cards."