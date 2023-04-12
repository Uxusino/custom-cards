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
    if session.get("userid") is not None:
        is_guest = False
    else:
        is_guest = True
    return render_template("profile.html", username=username, user=userid, packs=pack_list, is_guest=is_guest)

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
    username = session.get("username")
    if username is not None:
        url = f"/users/{username}"
        return redirect(f"{url}")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        new_user = users.new_user(username, password)
        success = new_user[0]
        if not success:
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
    check = session.get("userid")
    if not check:
        return redirect("/register")
    return render_template("create.html", languages=languages)

@app.route("/packs/<int:id>")
def pack(id):
    pack = packs.get_pack(id)
    if pack:
        userid = packs.get_owner(id)
    else:
        userid = None
    if session.get("userid") is not None:
        is_guest = False
    else:
        is_guest = True
    return render_template("pack.html", userid=userid, pack=pack, is_guest=is_guest)

@app.route("/edit_name", methods=["POST"])
def edit_name():
    name = request.form.get("name")
    id = request.form.get("id")
    packs.edit_name(pack_id=id, new_name=name)
    return redirect(f"/packs/{id}")

@app.route("/search")
def search():
    return "On this page you will be able to search for packs or other users."

@app.route("/simulator")
def simulator():
    return "This page will contain simulation of CAH, where you can test your cards."