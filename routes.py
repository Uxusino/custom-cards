from app import app, languages
from flask import render_template, request, redirect, flash, session

import users
import packs

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users/<string:username>")
def user(username):
    userid = users.get_userid(username)
    pack_list = packs.get_packs(userid)
    return render_template("profile.html", username=username, user=userid, current_user=session["username"], packs=pack_list)

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

@app.route("/logout")
def logout():
    users.logout()
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
            profile_url = "/users/" + username
            return redirect(profile_url)
    return render_template("register.html")

@app.route("/create", methods = ["GET", "POST"])
def create():
    if request.method == "POST":
        #token = request.form["crsf_token"]
        users.correct_csrf()
        userid = session["userid"]
        name = request.form["name"]
        language = request.form["language"]
        is_public = request.form["publicity"]
        if is_public == 1:
            is_public = True
        elif is_public == 0:
            is_public = False
        pack = packs.new_pack(userid, name, language, is_public)
        success = pack[0]
        if not success:
            error_msg = pack[1]
            flash(error_msg)
            return render_template("create.html", languages=languages)
        else:
            pack_id = pack[1]
            pack_url = "/packs/" + str(pack_id)
            return redirect(pack_url)
    return render_template("create.html", languages=languages)

@app.route("/packs/<int:id>")
def pack(id):
    pack = packs.get_pack(id)
    if pack:
        userid = packs.get_owner(id)
    else:
        userid = None
    return render_template("pack.html", userid=userid, pack=pack)

@app.route("/simulator")
def simulator():
    return "This page will contain simulation of CAH, where you can test your cards."