import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}

    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def add_review(title, author, year, description, user_id, classes):
    sql = "INSERT INTO reviews (title, author, year, description, user_id) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [title, author, year, description, user_id])

    review_id = db.last_insert_id()

    sql = "INSERT INTO review_classes (review_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql,[review_id, title, value])

def add_comment(review_id, user_id, comment):
    sql = "INSERT INTO comments (review_id, user_id, comment) VALUES (?, ?, ?)"
    db.execute(sql, [review_id, user_id, comment])

def get_comment(review_id):
    sql = """SELECT comments.comment, users.id user_id, users.username
            FROM comments, users
            WHERE comments.review_id = ? AND comments.user_id = users.id
            ORDER BY comments.id DESC"""
    return db.query(sql, [review_id])

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