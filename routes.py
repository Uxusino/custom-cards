from app import app, languages
from flask import render_template, request, redirect, flash, session, jsonify

import random
import json

import users
import packs
import reviews

@app.route("/")
def index():
    recent_packs = packs.get_recent_packs()
    return render_template("index.html", recent_packs=recent_packs)

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
    username = request.form.get("username")
    password = request.form.get("password")
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
        username = request.form.get("username")
        password = request.form.get("password")
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
        is_public = request.form.get("publicity") == "true"
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
    pack_id = request.form["id"]
    id = request.form["cardId"]
    content = request.form["name"]
    card = packs.edit_white_card(id, content)
    success = card[0]
    if not success:
        error_msg = card[1]
        flash(error_msg)
    return redirect(f"/packs/{pack_id}")

@app.route("/edit_black_card", methods=["POST"])
def edit_black_card():
    users.correct_csrf()
    pack_id = request.form["id"]
    id = request.form["cardId"]
    content = request.form["name"]
    card = packs.edit_black_card(id, content)
    success = card[0]
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
    current_userid = session.get("userid")
    if pack:
        userid = packs.get_owner(id)
    else:
        userid = None
    if current_userid is not None:
        is_guest = False
    else:
        is_guest = True
    white_cards = packs.get_white_cards(id)
    black_cards = packs.get_black_cards(id)
    revs = reviews.get_all_reviews(id)
    mean_rating = reviews.mean_rating(id)
    user_left_review = reviews.review_left(id, current_userid)
    # User's own review of the pack must always be placed on top.
    if user_left_review:
        i = 0
        for review in revs:
            if review['id'] == user_left_review:
                users_review = revs.pop(i)
                revs.insert(0, users_review)
                break
            i += 1
    return render_template("pack.html",
                           userid=userid,
                           pack=pack,
                           is_guest=is_guest,
                           languages=languages,
                           white_cards=white_cards,
                           black_cards=black_cards,
                           revs=revs,
                           mean_rating=mean_rating,
                           user_left_review=user_left_review,
                           )

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

@app.route("/rate_pack", methods=["POST"])
def rate_pack():
    users.correct_csrf()
    rating = int(request.form.get("rating"))
    comment = request.form.get("comment")
    pack_id = request.form.get("pack_id")
    author_id = request.form.get("author_id")
    reviews.new_review(user_id=author_id, pack_id=pack_id, rating=rating, comment=comment)
    return redirect(f"/packs/{pack_id}")

@app.route("/search")
def search():
    return render_template("search.html", packs=None, is_search=False)

@app.route("/search/<string:query>")
def search_q(query):
    _packs = packs.search_packs(query)
    return render_template("search.html", packs=_packs, is_search=True)

@app.route("/find_packs", methods=["POST"])
def find_packs():
    query = request.form.get("search")
    return redirect(f"/search/{query}")

@app.route("/simulator")
def simulator():
    _packs = packs.get_packs(session.get("userid"))
    return render_template("simulator-main.html", packs=_packs)

@app.route("/simulator/<int:id>", methods=["GET", "POST"])
def simulator_pack(id):
    if request.method == "POST":
        data = json.loads(request.data)
        black_card = data.get("blackcardraw", "")
        blanks = int(data.get("blackcardblanks", 0))
        white_cards = data.get("selectedCards", ["error"])
        result = packs.insert_into_black_card(black_card, white_cards, blanks)
        response = {
            "result": result
        }
        return jsonify(response)
    else:
        pack = packs.get_pack(id)
        if pack['white_cards'] < 10 or pack['black_cards'] == 0:
            return redirect("/simulator")
        if not pack["is_public"] and pack["author"] != session.get("username"):
            return redirect("/simulator")
        white_cards = packs.pick_white_cards(id)
        black_cards = packs.get_black_cards(id)
        random.shuffle(black_cards)
        return render_template("simulator.html", black_cards=black_cards, white_cards=white_cards, pack_id=id)