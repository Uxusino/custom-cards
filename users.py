from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db

# Returns (True, None) if succesfull and (False, error: str) otherwise
def new_user(username: str, password: str) -> tuple:
    # First check if both fields are non-empty
    if not username or not password:
        return (False, "Please fill both fields.")
    # Check if this user already exists
    if user_exists(username):
        return (False, "This user already exists.")
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password, is_admin) VALUES(:username, :password, false)")
    db.session.execute(sql, {"username": username, "password": hash_value})
    db.session.commit()
    return (True, None)

def user_exists(username: str) -> bool:
    sql = text("SELECT username FROM users WHERE lower(username)=:username")
    res = db.session.execute(sql, {"username": username.lower()})
    user = res.fetchone()
    if not user:
        return False
    return True