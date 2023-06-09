from datetime import datetime
from sqlalchemy.sql import text
from db import db, execute

import users

def new_review(user_id: int, pack_id: int, rating: int, comment: str):
    if not valid_comment(comment):
        return
    left_at = datetime.now()
    sql = text("INSERT INTO reviews (user_id, pack_id, rating, comment, time) VALUES (:user_id, :pack_id, :rating, :comment, :time)")
    params = {
        "user_id": user_id,
        "pack_id": pack_id,
        "rating": rating,
        "comment": comment,
        "time": left_at
    }
    execute(query=sql, params=params)
    db.session.commit()

def valid_comment(comment: str) -> bool:
    if len(comment) > 1000:
        return False
    return True

# Converts mean value to str altogether
def mean_rating(pack_id: int) -> str:
    sql = text("SELECT COALESCE(ROUND(SUM(rating)::numeric / COUNT(rating), 1), 0) FROM reviews WHERE pack_id=:pack_id")
    res = execute(sql, {"pack_id": pack_id})
    mean = res.fetchone()[0]
    if mean == 0:
        return "-"
    else:
        return str(mean)
    
def is_author(id: int) -> bool:
    sql = text("SELECT CASE WHEN r.user_id = p.author_id THEN TRUE ELSE FALSE END FROM reviews r, packs p WHERE r.id=:id AND r.pack_id=p.id")
    res = execute(sql, {"id": id})
    isAuthor = res.fetchone()[0]
    return isAuthor

def delete_review(pack_id: int, user_id: int) -> None:
    sql = text("DELETE FROM reviews WHERE pack_id=:pack_id AND user_id=:user_id")
    execute(sql, {"pack_id": pack_id, "user_id": user_id})
    db.session.commit()

def edit_review(pack_id: int, user_id: int, comment: str, rating: int) -> None:
    if not valid_comment(comment):
        return
    time = datetime.now()
    sql = text("UPDATE reviews SET comment=:comment, rating=:rating, time=:time WHERE pack_id=:pack_id AND user_id=:user_id")
    execute(sql, {
        "comment": comment,
        "rating": rating,
        "time": time,
        "pack_id": pack_id,
        "user_id": user_id
    })
    db.session.commit()

# Returns id of author's review, None if there is not
def review_left(pack_id: int, user_id: int) -> int | None:
    sql = text("SELECT id FROM reviews WHERE pack_id=:pack_id AND user_id=:user_id")
    res = execute(sql, {
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
    res = execute(sql, {"pack_id": pack_id})
    rows = res.fetchall()
    if not rows:
        return None
    reviews_list = []
    for review in rows:
        id = review[0]
        user_id = review[1]
        author = is_author(id)
        username = users.get_username(user_id)
        time = format_time(review[4])
        dictionary = {
            "id": id,
            "user_id": user_id,
            "username": username,
            "pack_id": pack_id,
            "rating": review[2],
            "comment": review[3],
            "time": time,
            "is_author": author
        }
        if author:
            reviews_list.insert(0, dictionary)
        else:
            reviews_list.append(dictionary)
    return reviews_list

def format_time(time: datetime) -> str:
    return time.strftime("%H:%M, %d/%m/%Y")