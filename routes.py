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
    pack_count = packs.count_packs(userid)
    if session.get("userid") is not None:
        is_guest = False
    else:
        is_guest = True
    return render_template("profile.html",
                           username=username,
                           user=userid,
                           packs=pack_list,
                           is_guest=is_guest,
                           pack_count=pack_count)

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

@app.route("/add_white_card", methods=["POST"])
def add_white_card():
    users.correct_csrf()
    content = request.form["white_card_content"]
    pack_id = request.form["pack_id"]
    card = packs.add_white_card(pack_id, content)
    success = card[0]
    if not success:
        error_msg = card[1]
        flash(error_msg)
    return redirect(f"/packs/{pack_id}")
    
@app.route("/add_black_card", methods=["POST"])
def add_black_card():
    users.correct_csrf()
    content = request.form["black_card_content"]
    pack_id = request.form["pack_id"]
    card = packs.add_black_card(pack_id, content)
    success = card[0]
    if not success:
        error_msg = card[1]
        flash(error_msg)
    return redirect(f"/packs/{pack_id}")

@app.route("/edit_white_card", methods=["POST"])
def edit_white_card():
    users.correct_csrf()
    id = request.form["white_card_id"]
    content = "Testing... ;)"
    card = packs.edit_white_card(id, content)
    success = card[0]
    pack_id = request.form["pack_id"]
    if not success:
        error_msg = card[1]
        flash(error_msg)
    return redirect(f"/packs/{pack_id}")

@app.route("/edit_black_card", methods=["POST"])
def edit_black_card():
    users.correct_csrf()
    id = request.form["black_card_id"]
    content = "Testing _ (;"
    card = packs.edit_black_card(id, content)
    success = card[0]
    pack_id = request.form["pack_id"]
    if not success:
        error_msg = card[1]
        flash(error_msg)
    return redirect(f"/packs/{pack_id}")

@app.route("/delete_white_card", methods=["POST"])
def delete_white_card():
    users.correct_csrf()
    id = request.form["white_card_id"]
    pack_id = request.form["pack_id"]
    packs.delete_white_card(id)
    return redirect(f"/packs/{pack_id}")

@app.route("/delete_black_card", methods=["POST"])
def delete_black_card():
    users.correct_csrf()
    id = request.form["black_card_id"]
    pack_id = request.form["pack_id"]
    packs.delete_black_card(id)
    return redirect(f"/packs/{pack_id}")

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
    white_cards = packs.get_white_cards(id)
    black_cards = packs.get_black_cards(id)
    return render_template("pack.html",
                           userid=userid,
                           pack=pack,
                           is_guest=is_guest,
                           languages=languages,
                           white_cards=white_cards,
                           black_cards=black_cards)

@app.route("/edit_name", methods=["POST"])
def edit_name():
    users.correct_csrf()
    name = request.form.get("name")
    id = request.form.get("id")
    packs.edit_name(pack_id=id, new_name=name)
    return redirect(f"/packs/{id}")

@app.route("/edit_language", methods=["POST"])
def edit_language():
    users.correct_csrf()
    language = request.form.get("language")
    id = request.form.get("id")
    packs.edit_language(pack_id=id, new_language=language)
    return redirect(f"/packs/{id}")

@app.route("/edit_privacy", methods=["POST"])
def edit_privacy():
    users.correct_csrf()
    privacy = request.form.get("privacy")
    if privacy == "true":
        privacy = True
    else:
        privacy = False
    id = request.form.get("id")
    packs.edit_publicity(pack_id=id, is_public=privacy)
    return redirect(f"/packs/{id}")

@app.route("/delete_pack", methods=["POST"])
def delete_pack():
    users.correct_csrf()
    id = request.form.get("id")
    packs.delete_pack(id)
    return redirect(f"/users/{session.get('username')}")

@app.route("/search")
def search():
    return "On this page you will be able to search for packs or other users."

@app.route("/simulator")
def simulator():
    return "This page will contain simulation of CAH, where you can test your cards."