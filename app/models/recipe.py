from datetime import datetime, timezone

from app.models.database import get_db


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


_SELECT_WITH_CATEGORY = """
    SELECT recipes.*, categories.name AS category_name
    FROM recipes
    LEFT JOIN categories ON categories.id = recipes.category_id
"""


def get_all(category_id=None):
    db = get_db()
    if category_id is None:
        return db.execute(
            _SELECT_WITH_CATEGORY + " ORDER BY recipes.created_at DESC"
        ).fetchall()
    return db.execute(
        _SELECT_WITH_CATEGORY
        + " WHERE recipes.category_id = ? ORDER BY recipes.created_at DESC",
        (category_id,),
    ).fetchall()


def get_by_id(recipe_id):
    db = get_db()
    return db.execute(
        _SELECT_WITH_CATEGORY + " WHERE recipes.id = ?", (recipe_id,)
    ).fetchone()


def create(data):
    db = get_db()
    now = _now()
    cursor = db.execute(
        """
        INSERT INTO recipes
            (title, description, ingredients, steps,
             prep_time_minutes, cook_time_minutes, servings, category_id,
             image_filename, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["title"],
            data.get("description"),
            data["ingredients"],
            data["steps"],
            data.get("prep_time_minutes"),
            data.get("cook_time_minutes"),
            data.get("servings"),
            data.get("category_id"),
            data.get("image_filename"),
            now,
            now,
        ),
    )
    db.commit()
    return cursor.lastrowid


def update(recipe_id, data):
    db = get_db()
    db.execute(
        """
        UPDATE recipes
        SET title = ?, description = ?, ingredients = ?, steps = ?,
            prep_time_minutes = ?, cook_time_minutes = ?, servings = ?,
            category_id = ?, image_filename = ?, updated_at = ?
        WHERE id = ?
        """,
        (
            data["title"],
            data.get("description"),
            data["ingredients"],
            data["steps"],
            data.get("prep_time_minutes"),
            data.get("cook_time_minutes"),
            data.get("servings"),
            data.get("category_id"),
            data.get("image_filename"),
            _now(),
            recipe_id,
        ),
    )
    db.commit()


def delete(recipe_id):
    db = get_db()
    db.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    db.commit()
