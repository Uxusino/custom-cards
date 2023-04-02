from datetime import datetime
from sqlalchemy.sql import text
from db import db

import users

# Returns (True, pack_id: int) if successfull, (False, error: str) otherwise
def new_pack(userid: int, name: str, language: str, is_public: bool) -> tuple:
    created_at = datetime.now()
    if not userid:
        return (False, "You must be logged in to create packs.")
    if name:
        pack_exists = get_pack_id(userid, name)
        if pack_exists:
            return (False, "You already have a pack with the same name.")
    else:
        username = users.get_username(userid)
        count = count_packs(userid) + 1
        name = f"{username}'s Pack №{count}"
    if not language:
        language = "Nevermind"
    sql = text("INSERT INTO packs (author_id, name, language, created, is_public) VALUES (:author_id, :name, :language, :created, :is_public)")
    db.session.execute(sql, {
        "author_id": userid,
        "name": name,
        "language": language,
        "created": created_at,
        "is_public": is_public
    })
    db.session.commit()
    id = get_pack_id(userid, name)
    return (True, id)

# Simply deletes a pack with certain id
def delete_pack(pack_id: int):
    sql = text("DELETE FROM packs WHERE id=:id")
    db.session.execute(sql, {"id": pack_id})
    db.session.commit()

### Functions for editing some values of a pack

def edit_name(pack_id: int, new_name: str):
    sql = text("UPDATE packs SET name=:name WHERE id=:id")
    db.session.execute(sql, {"name": new_name, "id": pack_id})
    db.session.commit()

def edit_language(pack_id: int, new_language: str):
    sql = text("UPDATE packs SET language=:language WHERE id=:id")
    db.session.execute(sql, {"language": new_language, "id": pack_id})
    db.session.commit()

def edit_publicity(pack_id: int, is_public: bool):
    sql = text("UPDATE packs SET is_public=:is_public WHERE id=:id")
    db.session.execute(sql, {"is_public": is_public, "id": pack_id})
    db.session.commit()

# Returns a list of dictionaries containing all packs by an user. Returns None, if this user has no packs
def get_packs(userid: int) -> list[dict] | None:
    author_name = users.get_username(userid)
    sql = text("SELECT id, name, language, created, is_public FROM packs WHERE author_id=:author_id ORDER BY id DESC")
    res = db.session.execute(sql, {"author_id": userid})
    if not res:
        return None
    packs = res.fetchall()
    packs_list = []
    for pack in packs:
        dictionary = {
            "id": pack[0],
            "author": author_name,
            "name": pack[1],
            "language": pack[2],
            "created": pack[3],
            "is_public": pack[4]
        }
        packs_list.append(dictionary)
    return packs_list

def get_pack(pack_id: int) -> dict | None:
    sql = text("SELECT author_id, name, language, created, is_public FROM packs WHERE id=:id")
    res = db.session.execute(sql, {"id": pack_id})
    pack = res.fetchone()
    if not pack:
        return None
    author = users.get_username(pack[0])
    return {
        "id": pack_id,
        "author": author,
        "name": pack[1],
        "language": pack[2],
        "created": pack[3],
        "is_public": pack[4]
    }

# Returns id if pack exists, None otherwise
def get_pack_id(author_id: int, name: str) -> int | None:
    sql = text("SELECT id FROM packs WHERE author_id=:author_id AND name=:name")
    res = db.session.execute(sql, {"author_id": author_id, "name": name})
    id = res.fetchone()
    if not id:
        return None
    return id[0]

def get_owner(pack_id: int) -> int | None:
    sql = text("SELECT u.id FROM users u, packs p WHERE p.id=:id AND p.author_id=u.id")
    res = db.session.execute(sql, {"id": pack_id})
    id = res.fetchone()
    if not id:
        return None
    return id[0]

def count_packs(userid: int) -> int:
    sql = text("SELECT COUNT(id) FROM packs WHERE author_id=:author_id")
    res = db.session.execute(sql, {"author_id": userid})
    count = res.fetchone()[0]
    return count