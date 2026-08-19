from app.models.database import get_db


def get_all():
    db = get_db()
    return db.execute("SELECT * FROM categories ORDER BY name ASC").fetchall()


def get_by_id(category_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM categories WHERE id = ?", (category_id,)
    ).fetchone()


def name_exists(name, exclude_id=None):
    db = get_db()
    if exclude_id is None:
        row = db.execute(
            "SELECT 1 FROM categories WHERE LOWER(name) = LOWER(?)", (name,)
        ).fetchone()
    else:
        row = db.execute(
            "SELECT 1 FROM categories WHERE LOWER(name) = LOWER(?) AND id != ?",
            (name, exclude_id),
        ).fetchone()
    return row is not None


def create(name):
    db = get_db()
    cursor = db.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    db.commit()
    return cursor.lastrowid


def update(category_id, name):
    db = get_db()
    db.execute(
        "UPDATE categories SET name = ? WHERE id = ?", (name, category_id)
    )
    db.commit()


def delete(category_id):
    db = get_db()
    db.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    db.commit()
