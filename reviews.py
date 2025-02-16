import db


def add_review(title, author, year, description, user_id, classes):
    sql = "INSERT INTO reviews (title, author, year, description, user_id) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [title, author, year, description, user_id])

    review_id = db.last_insert_id()

    sql = "INSERT INTO review_classes (review_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql,[review_id, title, value])


def get_classes(review_id):
    sql = "SELECT title, value FROM review_classes WHERE review_id = ?"
    return db.query(sql, [review_id])


def get_reviews():
    sql = "SELECT id, title, author, year FROM reviews ORDER by id DESC"
    return db.query(sql)

def get_review(review_id):
    sql = """SELECT reviews.id, reviews.title, reviews.author, reviews.year, reviews.description, users.id user_id, users.username

            FROM reviews, users
            WHERE reviews.user_id = users.id
            AND reviews.id = ? """

    return db.query(sql, [review_id])[0]


def update_review(review_id, title, author, year, description):
    sql = """UPDATE reviews SET title = ?,
                                author = ?,
                                year = ?,
                                description = ?,
                            WHERE id = ?"""

    db.execute(sql, [title, author, year, description, review_id])


def remove_review(review_id):
    sql = "DELETE FROM reviews WHERE id = ?"
    db.execute(sql, [review_id])


def find_reviews(query):
    sql = """SELECT id, title
            FROM reviews
            WHERE title LIKE ? OR description LIKE ?
            ORDER BY id DESC"""

    return db.query(sql, ["%" + query + "%", "%" + query + "%"])