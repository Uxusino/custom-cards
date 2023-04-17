from datetime import datetime
from sqlalchemy.sql import text
from db import db

import users
import re

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

def add_white_card(pack_id: int, content: str) -> tuple:
    check = check_card_content(content)
    if not check:
        return (False, "Card lenght must be at least 1 symbol and at most 50 symbols long.")
    sql = text("INSERT INTO white_cards (pack_id, content) VALUES (:pack_id, :content)")
    db.session.execute(sql, {
        "pack_id": pack_id,
        "content": content
    })
    db.session.commit()
    return (True, None)

def check_card_content(content) -> tuple:
    if len(content) < 1 or len(content) > 50:
        return False
    return True

def delete_white_card(id: int) -> None:
    sql = text("DELETE FROM white_cards WHERE id=:id")
    db.session.execute(sql, {
        "id": id
    })
    db.session.commit()

def edit_white_card(id: int, new_content: str) -> None:
    check = check_card_content(new_content)
    if not check:
        return (False, "Card lenght must be at least 1 symbol and at most 50 symbols long.")
    sql = text("UPDATE white_cards SET content=:new_content WHERE id=:id")
    db.session.execute(sql, {
        "new_content": new_content,
        "id": id
    })
    db.session.commit()
    return (True, None)

# If you want underscore to be a part of the text, write it like /_
def parse_black_card(content: str) -> tuple:
    # Makes all underscores 1 symbol long
    new_content = re.sub(r"(?<!/)_+", "_", content)
    # Counts all matches that could be inserted into in future
    count = len(re.findall(r"(?<!/)_+", new_content))
    return (new_content, count)

def black_card_display(content: str) -> str:
    return content.replace("/_", "_")

def add_black_card(pack_id: int, content: str) -> tuple:
    check = check_card_content(content)
    if not check:
        return (False, "Card lenght must be at least 1 symbol and at most 50 symbols long.")
    sql = text("INSERT INTO black_cards (pack_id, content, blanks) VALUES (:pack_id, :content, :blanks)")
    parse = parse_black_card(content)
    content = parse[0]
    blanks = parse[1]
    db.session.execute(sql, {
        "pack_id": pack_id,
        "content": content,
        "blanks": blanks
    })
    db.session.commit()
    return (True, None)

def delete_black_card(id: int) -> None:
    sql = text("DELETE FROM black_cards WHERE id=:id")
    db.session.execute(sql, {
        "id": id
    })
    db.session.commit()

def edit_black_card(id: int, new_content: str) -> None:
    check = check_card_content(new_content)
    if not check:
        return (False, "Card lenght must be at least 1 symbol and at most 50 symbols long.")
    sql = text("UPDATE black_cards SET content=:new_content, blanks=:blanks WHERE id=:id")
    parsed = parse_black_card(new_content)
    new_content = parsed[0]
    blanks = parsed[1]
    db.session.execute(sql, {
        "new_content": new_content,
        "blanks": blanks,
        "id": id
    })
    db.session.commit()
    return (True, None)

# Inserts words into underscores and lives /_ untouched.
def insert_into_black_card(black_content: str, white_content: list[str], blanks: int) -> str:
    if len(white_content) != blanks:
        return None
    if blanks == 0:
        blanks = 1
        black_content = black_content + "_"
    innocent_slashes = re.findall(r"/_+", black_content)
    print(innocent_slashes)
    black_content_temp = re.sub(r"/_+", "[%ACTUALLY-JUST-A-PLACEHOLDER%]", black_content)

    y = 0
    x = 0
    while x < len(black_content_temp) and y < blanks:
        if black_content_temp[x] == "_":
            black_content_temp = black_content_temp[:x] + white_content[y] + black_content_temp[x+1:]
            x += len(white_content[y]) - 1
            y += 1
        x += 1

    if len(innocent_slashes) != 0:
        black_content_list = black_content_temp.split("[%ACTUALLY-JUST-A-PLACEHOLDER%]")
        black_content_temp = black_content_list[0]
        for z in range(len(innocent_slashes)):
            black_content_temp += innocent_slashes[z] + black_content_list[z+1]
    return black_content_temp

def get_white_cards(pack_id: int) -> list[dict] | None:
    sql = text("SELECT id, content FROM white_cards WHERE pack_id=:pack_id ORDER BY id DESC")
    res = db.session.execute(sql, {"pack_id": pack_id})
    if not res:
        return None
    cards = res.fetchall()
    cards_list = []
    for card in cards:
        dictionary = {
            "id": card[0],
            "content": card[1]
        }
        cards_list.append(dictionary)
    return cards_list

def get_black_cards(pack_id: int) -> list[dict] | None:
    sql = text("SELECT id, content FROM black_cards WHERE pack_id=:pack_id ORDER BY id DESC")
    res = db.session.execute(sql, {"pack_id": pack_id})
    if not res:
        return None
    cards = res.fetchall()
    cards_list = []
    for card in cards:
        dictionary = {
            "id": card[0],
            "content": black_card_display(card[1])
        }
        cards_list.append(dictionary)
    return cards_list

# Simply deletes a pack with certain id
def delete_pack(pack_id: int):
    delete_white_cards = text("DELETE FROM white_cards WHERE pack_id=:pack_id")
    delete_black_cards = text("DELETE FROM black_cards WHERE pack_id=:pack_id")
    sql = text("DELETE FROM packs WHERE id=:id")
    db.session.execute(delete_white_cards, {"pack_id": pack_id})
    db.session.execute(delete_black_cards, {"pack_id": pack_id})
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

# Testing area
if __name__ == "__main__":
    bc = "/_Today I/___will//eat _ with/_ my _ while _"
    wc = ["apple", "banana", "petting a cat"]
    blanks = 3
    print(black_card_display(insert_into_black_card(bc, wc, blanks)))
    