CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);


CREATE TABLE reviews(
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    year INTEGER,
    genre TEXT,
    description TEXT,
    stars INTEGER,
    user_id INTEGER REFERENCES users
);
