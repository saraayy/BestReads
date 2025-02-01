import db


def add_review(title, author, year, genre, description, stars, user_id):
    sql = "INSERT INTO reviews (title, author, year, genre, description, stars, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
    db.execute(sql, [title, author, year, genre, description, stars, user_id])