CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);


CREATE TABLE reviews_new(
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    year INTEGER,
    description TEXT,
    user_id INTEGER REFERENCES users
);


CREATE TABLE review_classes (
    id INTEGER PRIMARY KEY,
    review_id INTEGER REFERENCES reviews,
    title TEXT,
    value TEXT
);