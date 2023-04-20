from datetime import datetime
from sqlalchemy.sql import text
from db import db

import users

def new_review(user_id: int, pack_id: int, rating: int, comment: str):
    if not valid_comment(comment):
        return
    left_at = datetime.now()
    sql = text("INSERT INTO reviews (user_id, pack_id, rating, comment, time) VALUES (:user_id, :pack_id, :rating, :comment, :time)")
    db.session.execute(sql, {
        "user_id": user_id,
        "pack_id": pack_id,
        "rating": rating,
        "comment": comment,
        "time": left_at
    })
    db.session.commit()

def valid_comment(comment: str) -> bool:
    if len(comment) > 1000:
        return False
    return True

# Converts mean to str altogether
def mean_rating(pack_id: int) -> str:
    sql = text("SELECT COALESCE(SUM(rating)/COUNT(rating), 0) FROM reviews WHERE pack_id=:pack_id")
    res = db.session.execute(sql, {"pack_id": pack_id})
    mean = res.fetchone()[0]
    if mean == 0:
        return "-"
    else:
        return str(mean)
    
def is_author(id: int) -> bool:
    sql = text("SELECT CASE WHEN r.user_id = p.author_id THEN TRUE ELSE FALSE END FROM reviews r, packs p WHERE r.id=:id AND r.pack_id=p.id")
    res = db.session.execute(sql, {"id": id})
    author = res.fetchone()[0]
    if author == 'true':
        return True
    return False

def delete_review(id: int):
    sql = text("DELETE FROM reviews WHERE id=:id")
    db.session.execute(sql, {"id": id})
    db.session.commit()

def edit_review(id: int, comment: str):
    sql = text("UPDATE reviews SET comment=:comment WHERE id=:id")
    db.session.execute(sql, {
        "comment": comment,
        "id": id
    })
    db.session.commit()

# Returns id of author's review, None if there is not
def review_left(pack_id: int, user_id: int) -> int | None:
    sql = text("SELECT id FROM reviews WHERE pack_id=:pack_id AND user_id=:user_id")
    res = db.session.execute(sql, {
        "pack_id": pack_id,
        "user_id": user_id
    })
    row = res.fetchone()
    if not row:
        return None
    id = row[0]
    return id

# Gets all reviews of a certain pack.
# Tries to place author's own review first.
def get_all_reviews(pack_id: int) -> list[dict] | None:
    sql = text("SELECT id, user_id, rating, comment, time FROM reviews WHERE pack_id=:pack_id ORDER BY time DESC")
    res = db.session.execute(sql, {"pack_id": pack_id})
    rows = res.fetchall()
    if not rows:
        return None
    reviews_list = []
    for review in rows:
        id = review[0]
        user_id = review[1]
        author = is_author(id)
        username = users.get_username(user_id)
        dictionary = {
            "id": id,
            "user_id": user_id,
            "username": username,
            "pack_id": pack_id,
            "rating": review[2],
            "comment": review[3],
            "time": review[4],
            "is_author": author
        }
        if author:
            reviews_list.insert(0, dictionary)
        else:
            reviews_list.append(dictionary)
    return reviews_list