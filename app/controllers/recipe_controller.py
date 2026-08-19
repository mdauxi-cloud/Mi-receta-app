import uuid
from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.models import category as category_model
from app.models import recipe as recipe_model

recipes_bp = Blueprint("recipes", __name__, url_prefix="/recetas")

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "svg", "webp"}


def _upload_dir():
    return Path(current_app.static_folder) / "uploads"


def _save_image(file_storage):
    filename = file_storage.filename
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return None, "Formato de imagen no permitido (usa png, jpg, gif, svg o webp)."
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    file_storage.save(_upload_dir() / new_filename)
    return f"uploads/{new_filename}", None


def _delete_image(image_path):
    if not image_path or not image_path.startswith("uploads/"):
        return
    path = Path(current_app.static_folder) / image_path
    if path.exists():
        path.unlink()


def _parse_form(form):
    errors = {}

    title = form.get("title", "").strip()
    if not title:
        errors["title"] = "El título es obligatorio."

    ingredients = form.get("ingredients", "").strip()
    if not ingredients:
        errors["ingredients"] = "Añade al menos un ingrediente."

    steps = form.get("steps", "").strip()
    if not steps:
        errors["steps"] = "Añade al menos un paso."

    def _parse_int(field_name, label):
        raw = form.get(field_name, "").strip()
        if not raw:
            return None
        try:
            value = int(raw)
        except ValueError:
            errors[field_name] = f"{label} debe ser un número entero."
            return None
        if value < 0:
            errors[field_name] = f"{label} no puede ser negativo."
            return None
        return value

    prep_time_minutes = _parse_int("prep_time_minutes", "El tiempo de preparación")
    cook_time_minutes = _parse_int("cook_time_minutes", "El tiempo de cocción")
    servings = _parse_int("servings", "Las porciones")

    category_id_raw = form.get("category_id", "").strip()
    category_id = None
    if category_id_raw:
        try:
            category_id = int(category_id_raw)
        except ValueError:
            errors["category_id"] = "Categoría no válida."
        else:
            if category_model.get_by_id(category_id) is None:
                errors["category_id"] = "La categoría seleccionada no existe."

    data = {
        "title": title,
        "description": form.get("description", "").strip() or None,
        "ingredients": ingredients,
        "steps": steps,
        "prep_time_minutes": prep_time_minutes,
        "cook_time_minutes": cook_time_minutes,
        "servings": servings,
        "category_id": category_id,
    }
    return data, errors


@recipes_bp.get("")
def list_recipes():
    category_id_raw = request.args.get("category_id", "").strip()
    category_id = int(category_id_raw) if category_id_raw.isdigit() else None
    recipes = recipe_model.get_all(category_id=category_id)
    categories = category_model.get_all()
    return render_template(
        "recipes/list.html",
        recipes=recipes,
        categories=categories,
        selected_category_id=category_id,
    )


@recipes_bp.get("/nueva")
def new_recipe():
    categories = category_model.get_all()
    return render_template(
        "recipes/form.html", recipe=None, errors={}, categories=categories
    )


@recipes_bp.post("/nueva")
def create_recipe():
    data, errors = _parse_form(request.form)

    image_filename = None
    image_file = request.files.get("image")
    if image_file and image_file.filename:
        image_filename, image_error = _save_image(image_file)
        if image_error:
            errors["image"] = image_error

    if errors:
        _delete_image(image_filename)
        categories = category_model.get_all()
        return render_template(
            "recipes/form.html", recipe=data, errors=errors, categories=categories
        ), 400

    data["image_filename"] = image_filename
    recipe_id = recipe_model.create(data)
    flash("Receta creada correctamente.", "success")
    return redirect(url_for("recipes.detail_recipe", recipe_id=recipe_id))


@recipes_bp.get("/<int:recipe_id>")
def detail_recipe(recipe_id):
    recipe = recipe_model.get_by_id(recipe_id)
    if recipe is None:
        flash("La receta solicitada no existe.", "error")
        return redirect(url_for("recipes.list_recipes"))
    return render_template("recipes/detail.html", recipe=recipe)


@recipes_bp.get("/<int:recipe_id>/editar")
def edit_recipe(recipe_id):
    recipe = recipe_model.get_by_id(recipe_id)
    if recipe is None:
        flash("La receta solicitada no existe.", "error")
        return redirect(url_for("recipes.list_recipes"))
    categories = category_model.get_all()
    return render_template(
        "recipes/form.html", recipe=recipe, errors={}, categories=categories
    )


@recipes_bp.post("/<int:recipe_id>/editar")
def update_recipe(recipe_id):
    existing = recipe_model.get_by_id(recipe_id)
    if existing is None:
        flash("La receta solicitada no existe.", "error")
        return redirect(url_for("recipes.list_recipes"))

    data, errors = _parse_form(request.form)

    new_image_filename = None
    image_file = request.files.get("image")
    if image_file and image_file.filename:
        new_image_filename, image_error = _save_image(image_file)
        if image_error:
            errors["image"] = image_error

    if errors:
        _delete_image(new_image_filename)
        data["id"] = recipe_id
        categories = category_model.get_all()
        return render_template(
            "recipes/form.html", recipe=data, errors=errors, categories=categories
        ), 400

    if new_image_filename:
        _delete_image(existing["image_filename"])
        data["image_filename"] = new_image_filename
    else:
        data["image_filename"] = existing["image_filename"]

    recipe_model.update(recipe_id, data)
    flash("Receta actualizada correctamente.", "success")
    return redirect(url_for("recipes.detail_recipe", recipe_id=recipe_id))


@recipes_bp.post("/<int:recipe_id>/eliminar")
def delete_recipe(recipe_id):
    recipe = recipe_model.get_by_id(recipe_id)
    if recipe is None:
        flash("La receta solicitada no existe.", "error")
        return redirect(url_for("recipes.list_recipes"))

    _delete_image(recipe["image_filename"])
    recipe_model.delete(recipe_id)
    flash("Receta eliminada.", "success")
    return redirect(url_for("recipes.list_recipes"))
