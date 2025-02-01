CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);


CREATE TABLE items(
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    year INTEGER,
    genre TEXT,
    description TEXT,
    stars INTEGER,
    user_id INTEGER REFRENCES users
);
