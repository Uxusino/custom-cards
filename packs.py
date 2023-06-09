from datetime import datetime
from sqlalchemy.sql import text
from db import db, execute

import users
import reviews
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
    params = {
        "author_id": userid,
        "name": name,
        "language": language,
        "created": created_at,
        "is_public": is_public
    }
    execute(sql, params)
    db.session.commit()
    id = get_pack_id(userid, name)
    return (True, id)

def add_white_card(pack_id: int, content: str) -> tuple:
    check = check_white_card(content)
    if not check:
        return (False, "Card lenght must be at least 1 symbol and at most 50 symbols long.")
    sql = text("INSERT INTO white_cards (pack_id, content) VALUES (:pack_id, :content)")
    execute(sql, {
        "pack_id": pack_id,
        "content": content
    })
    db.session.commit()
    return (True, None)

def check_white_card(content) -> bool:
    if len(content) < 1 or len(content) > 50:
        return False
    return True

def check_black_card(content) -> bool:
    if len(content) < 1 or len(content) > 120:
        return False
    return True

def delete_white_card(id: int) -> None:
    sql = text("DELETE FROM white_cards WHERE id=:id")
    execute(sql, {
        "id": id
    })
    db.session.commit()

def edit_white_card(id: int, new_content: str) -> None:
    check = check_white_card(new_content)
    if not check:
        return (False, "Card lenght must be at least 1 symbol and at most 50 symbols long.")
    sql = text("UPDATE white_cards SET content=:new_content WHERE id=:id")
    execute(sql, {
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
    check = check_black_card(content)
    if not check:
        return (False, "Card lenght must be at least 1 symbol and at most 120 symbols long.")
    sql = text("INSERT INTO black_cards (pack_id, content, blanks) VALUES (:pack_id, :content, :blanks)")
    parse = parse_black_card(content)
    content = parse[0]
    blanks = parse[1]
    execute(sql, {
        "pack_id": pack_id,
        "content": content,
        "blanks": blanks
    })
    db.session.commit()
    return (True, None)

def delete_black_card(id: int) -> None:
    sql = text("DELETE FROM black_cards WHERE id=:id")
    execute(sql, {
        "id": id
    })
    db.session.commit()

def edit_black_card(id: int, new_content: str) -> None:
    check = check_black_card(new_content)
    if not check:
        return (False, "Card lenght must be at least 1 symbol and at most 120 symbols long.")
    sql = text("UPDATE black_cards SET content=:new_content, blanks=:blanks WHERE id=:id")
    parsed = parse_black_card(new_content)
    new_content = parsed[0]
    blanks = parsed[1]
    execute(sql, {
        "new_content": new_content,
        "blanks": blanks,
        "id": id
    })
    db.session.commit()
    return (True, None)

# Inserts words into underscores and leaves /_ untouched.
def insert_into_black_card(black_content: str, white_content: list[str], blanks: int) -> str:
    if blanks == 0:
        blanks = 1
        black_content = black_content + " _"
    if len(white_content) != blanks:
        return None
    white_content = [card[:-1] if card[-1] == '.' else card for card in white_content]
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
    black_content_temp = black_content_temp.replace("/_", "_")
    return black_content_temp

def get_white_cards(pack_id: int) -> list[dict] | None:
    sql = text("SELECT id, content FROM white_cards WHERE pack_id=:pack_id ORDER BY id DESC")
    res = execute(sql, {"pack_id": pack_id})
    if not res:
        return None
    cards = res.fetchall()
    cards_list = [{"id": card[0], "content": card[1]} for card in cards]
    return cards_list

# Pick white cards in random order and returns them as a list of strings
def pick_white_cards(pack_id: int) -> list[str] | None:
    sql = text("SELECT content FROM white_cards WHERE pack_id=:pack_id ORDER BY RANDOM()")
    res = execute(sql, {"pack_id": pack_id})
    if not res:
        return None
    cards = res.fetchall()
    cards_list = [card[0] for card in cards]
    return cards_list

def get_black_cards(pack_id: int) -> list[dict] | None:
    sql = text("SELECT id, content, blanks FROM black_cards WHERE pack_id=:pack_id ORDER BY id DESC")
    res = execute(sql, {"pack_id": pack_id})
    if not res:
        return None
    cards = res.fetchall()
    cards_list = []
    for card in cards:
        dictionary = {
            "id": card[0],
            "content": black_card_display(card[1]),
            "content-unparsed": card[1],
            "blanks": card[2]
        }
        cards_list.append(dictionary)
    return cards_list

# Simply deletes a pack with certain id
def delete_pack(pack_id: int):
    delete_white_cards = text("DELETE FROM white_cards WHERE pack_id=:pack_id")
    delete_black_cards = text("DELETE FROM black_cards WHERE pack_id=:pack_id")
    delete_reviews = text("DELETE FROM reviews WHERE pack_id=:pack_id")
    sql = text("DELETE FROM packs WHERE id=:id")
    execute(delete_white_cards, {"pack_id": pack_id})
    execute(delete_black_cards, {"pack_id": pack_id})
    execute(delete_reviews, {"pack_id": pack_id})
    execute(sql, {"id": pack_id})
    db.session.commit()

### Functions for editing some values of a pack

def edit_name(pack_id: int, new_name: str):
    sql = text("UPDATE packs SET name=:name WHERE id=:id")
    execute(sql, {"name": new_name, "id": pack_id})
    db.session.commit()

def edit_language(pack_id: int, new_language: str):
    sql = text("UPDATE packs SET language=:language WHERE id=:id")
    execute(sql, {"language": new_language, "id": pack_id})
    db.session.commit()

def edit_publicity(pack_id: int, is_public: bool):
    sql = text("UPDATE packs SET is_public=:is_public WHERE id=:id")
    execute(sql, {"is_public": is_public, "id": pack_id})
    db.session.commit()

def pack_dict(id: int, author: str, name: str, language: str, created: str, is_public: bool, rating: str, white_cards: int, black_cards: int) -> dict:
    return {
        "id": id,
        "author": author,
        "name": name,
        "language": language,
        "created": created,
        "is_public": is_public,
        "rating": rating,
        "white_cards": white_cards,
        "black_cards": black_cards
    }

# Returns a list of dictionaries containing all packs by an user. Returns None, if this user has no packs
def get_packs(userid: int) -> list[dict] | None:
    author_name = users.get_username(userid)
    sql = text("SELECT id, name, language, created, is_public FROM packs WHERE author_id=:author_id ORDER BY id DESC")
    res = execute(sql, {"author_id": userid})
    if not res:
        return None
    packs = res.fetchall()
    packs_list = []
    for pack in packs:
        id = pack[0]
        rating = reviews.mean_rating(id)
        created = reviews.format_time(pack[3])
        dictionary = pack_dict(id, author_name, pack[1], pack[2], created, pack[4], rating, count_white_cards(id), count_black_cards(id))
        packs_list.append(dictionary)
    return packs_list

def get_pack(pack_id: int) -> dict | None:
    sql = text("SELECT author_id, name, language, created, is_public FROM packs WHERE id=:id")
    res = execute(sql, {"id": pack_id})
    pack = res.fetchone()
    if not pack:
        return None
    author = users.get_username(pack[0])
    rating = reviews.mean_rating(pack_id)
    created = reviews.format_time(pack[3])
    dictionary = pack_dict(pack_id, author, pack[1], pack[2], created, pack[4], rating, count_white_cards(pack_id), count_black_cards(pack_id))
    return dictionary

# Gets 20 the most recent packs.
def get_recent_packs() -> list[dict] | None:
    sql = text("SELECT id, author_id, name, language, created FROM packs WHERE is_public=TRUE ORDER BY created DESC LIMIT 20")
    res = execute(sql)
    packs = res.fetchall()
    if not packs:
        return None
    packs_list = []
    for pack in packs:
        id = pack[0]
        author_name = users.get_username(pack[1])
        created = reviews.format_time(pack[4])
        rating = reviews.mean_rating(id)
        dictionary = pack_dict(id, author_name, pack[2], pack[3], created, True, rating, count_white_cards(id), count_black_cards(id))
        packs_list.append(dictionary)
    return packs_list
        
# Returns id if pack exists, None otherwise
def get_pack_id(author_id: int, name: str) -> int | None:
    sql = text("SELECT id FROM packs WHERE author_id=:author_id AND name=:name")
    res = execute(sql, {"author_id": author_id, "name": name})
    id = res.fetchone()
    if not id:
        return None
    return id[0]

def search_packs(query: str) -> list[dict] | None:
    sql = text("SELECT p.id, p.author_id, p.name, p.language, p.created, p.is_public FROM packs p JOIN users u ON p.author_id=u.id WHERE p.is_public=TRUE AND (p.name ~* :query OR p.language ~* :query OR u.username ~* :query)")
    res = execute(sql, {"query": query})
    packs = res.fetchall()
    if not packs:
        return None
    packs_list = []
    for pack in packs:
        author_name = users.get_username(pack[1])
        created = reviews.format_time(pack[4])
        id = pack[0]
        rating = reviews.mean_rating(id)
        dictionary = pack_dict(id, author_name, pack[2], pack[3], created, pack[5], rating, count_white_cards(id), count_black_cards(id))
        packs_list.append(dictionary)
    return packs_list

def get_owner(pack_id: int) -> int | None:
    sql = text("SELECT u.id FROM users u, packs p WHERE p.id=:id AND p.author_id=u.id")
    res = execute(sql, {"id": pack_id})
    id = res.fetchone()
    if not id:
        return None
    return id[0]

def count_packs(userid: int) -> int:
    sql = text("SELECT COUNT(id) FROM packs WHERE author_id=:author_id")
    res = execute(sql, {"author_id": userid})
    count = res.fetchone()[0]
    return count

def count_white_cards(pack_id: int) -> int:
    sql = text("SELECT COUNT(id) FROM white_cards WHERE pack_id=:pack_id")
    res = execute(sql, {"pack_id": pack_id})
    count = res.fetchone()[0]
    return count

def count_black_cards(pack_id: int) -> int:
    sql = text("SELECT COUNT(id) FROM black_cards WHERE pack_id=:pack_id")
    res = execute(sql, {"pack_id": pack_id})
    count = res.fetchone()[0]
    return count

# Testing area
if __name__ == "__main__":
    bc = "Who's knocking at my door?"
    wc = ["apple"]
    blanks = 0
    print(black_card_display(insert_into_black_card(bc, wc, blanks)))
    