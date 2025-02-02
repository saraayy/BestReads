import db


def add_review(title, author, year, genre, description, stars, user_id):
    sql = "INSERT INTO reviews (title, author, year, genre, description, stars, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
    db.execute(sql, [title, author, year, genre, description, stars, user_id])

def get_reviews():
    sql = "SELECT id, title, author, year, genre FROM reviews ORDER by id DESC"
    return db.query(sql)

def get_review(review_id):
    sql = """SELECT reviews.title, reviews.author, reviews.year, reviews.genre, reviews.description, reviews.stars, users.username

            FROM reviews, users
            WHERE reviews.user_id = users.id
            AND reviews.id = ? """

    return db.query(sql, [review_id])[0]