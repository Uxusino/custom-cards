from flask import session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db, execute

import secrets
import string

# Returns (True, None) if succesfull and (False, error: str) otherwise
def new_user(username: str, password: str) -> tuple:
    # First check if both fields are non-empty
    if not username or not password:
        return (False, "Please fill both fields.")
    # Check if this user already exists
    if get_userid(username):
        return (False, "This user already exists.")
    if len(username) < 4 or len(username) > 30:
        return (False, "Your username must contain from 4 to 30 symbols.")
    if len(password) < 6:
        return(False, "Your password must be at least 6 symbols long.")
    if not good_chars(username):
        return (False, "You can use some special symbols in your username, but not SO special...")
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password, is_admin) VALUES(:username, :password, false)")
    execute(sql, {"username": username, "password": hash_value})
    db.session.commit()
    login(username, password)
    return (True, None)

def good_chars(username):
    allowed = string.ascii_letters + string.digits + string.punctuation
    if any(char not in allowed for char in username):
        return False
    return True

# Returns (True, None) if succesfull and (False, error: str) otherwise
def login(username: str, password: str) -> tuple:
    id = get_userid(username)
    if id:
        hash_value = get_hashed_password(id)
        if check_password_hash(hash_value, password):
            session["userid"] = id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return (True, None)
    return (False, "Invalid username or password.")

def logout() -> None:
    del session["userid"]
    del session["username"]
    del session["csrf_token"]

def correct_csrf():
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)

# Returns user id if user exists, None otherwise
def get_userid(username: str) -> int:
    sql = text("SELECT id FROM users WHERE lower(username)=:username")
    res = execute(sql, {"username": username.lower()})
    id = res.fetchone()
    if not id:
        return None
    return id[0]

def get_username(userid: int) -> str:
    sql = text("SELECT username FROM users WHERE id=:id")
    res = execute(sql, {"id": userid})
    username = res.fetchone()
    if not username:
        return None
    return username[0]

def get_hashed_password(userid: int) -> str:
    sql = text("SELECT password FROM users WHERE id=:id")
    res = execute(sql, {"id": userid})
    h_password = res.fetchone()[0]
    return h_password