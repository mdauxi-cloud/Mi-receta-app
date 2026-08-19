from datetime import datetime, timezone

from app.models.database import get_db


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_all():
    db = get_db()
    return db.execute(
        "SELECT * FROM recipes ORDER BY created_at DESC"
    ).fetchall()


def get_by_id(recipe_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM recipes WHERE id = ?", (recipe_id,)
    ).fetchone()


def create(data):
    db = get_db()
    now = _now()
    cursor = db.execute(
        """
        INSERT INTO recipes
            (title, description, ingredients, steps,
             prep_time_minutes, cook_time_minutes, servings,
             created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["title"],
            data.get("description"),
            data["ingredients"],
            data["steps"],
            data.get("prep_time_minutes"),
            data.get("cook_time_minutes"),
            data.get("servings"),
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
            updated_at = ?
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
            _now(),
            recipe_id,
        ),
    )
    db.commit()


def delete(recipe_id):
    db = get_db()
    db.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    db.commit()
