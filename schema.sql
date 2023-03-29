CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL
);

CREATE TABLE packs (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES users,
    name TEXT,
    language TEXT,
    created TIMESTAMP,
    is_public BOOLEAN NOT NULL
);

CREATE TABLE white_cards (
    id SERIAL PRIMARY KEY,
    pack_id INTEGER REFERENCES packs,
    content TEXT NOT NULL
);

CREATE TABLE black_cards (
    id SERIAL PRIMARY KEY,
    pack_id INTEGER REFERENCES packs,
    content TEXT NOT NULL,
    blanks INTEGER
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    pack_id INTEGER REFERENCES packs,
    rating INTEGER,
    comment TEXT
);