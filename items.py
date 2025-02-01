import db


def add_item(title, author, year, genre, description, stars, user_id):
    sql = "INSERT INTO items (title, author, year, genre, description, stars, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
    db.execute(sql, [title, author, year, genre, description, stars, user_id])