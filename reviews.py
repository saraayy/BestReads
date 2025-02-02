import db


def add_review(title, author, year, genre, description, stars, user_id):
    sql = "INSERT INTO reviews (title, author, year, genre, description, stars, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
    db.execute(sql, [title, author, year, genre, description, stars, user_id])

def get_reviews():
    sql = "SELECT id, title, author, year, genre FROM reviews ORDER by id DESC"
    return db.query(sql)

def get_review(review_id):
    sql = """SELECT reviews.id, reviews.title, reviews.author, reviews.year, reviews.genre, reviews.description, reviews.stars, users.id user_id, users.username

            FROM reviews, users
            WHERE reviews.user_id = users.id
            AND reviews.id = ? """

    return db.query(sql, [review_id])[0]


def update_review(review_id, title, author, year, genre, description, stars):
    sql = """UPDATE reviews SET title = ?,
                                author = ?,
                                year = ?,
                                genre = ?,
                                description = ?,
                                stars = ?
                            WHERE id = ?"""

    db.execute(sql, [title, author, year, genre, description, stars, review_id])





def remove_review(review_id):
    sql = "DELETE FROM reviews WHERE id = ?"
    db.execute(sql, [review_id])