from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models import category as category_model
from app.models import recipe as recipe_model

recipes_bp = Blueprint("recipes", __name__, url_prefix="/recetas")


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
    if errors:
        categories = category_model.get_all()
        return render_template(
            "recipes/form.html", recipe=data, errors=errors, categories=categories
        ), 400

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
    if recipe_model.get_by_id(recipe_id) is None:
        flash("La receta solicitada no existe.", "error")
        return redirect(url_for("recipes.list_recipes"))

    data, errors = _parse_form(request.form)
    if errors:
        data["id"] = recipe_id
        categories = category_model.get_all()
        return render_template(
            "recipes/form.html", recipe=data, errors=errors, categories=categories
        ), 400

    recipe_model.update(recipe_id, data)
    flash("Receta actualizada correctamente.", "success")
    return redirect(url_for("recipes.detail_recipe", recipe_id=recipe_id))


@recipes_bp.post("/<int:recipe_id>/eliminar")
def delete_recipe(recipe_id):
    if recipe_model.get_by_id(recipe_id) is None:
        flash("La receta solicitada no existe.", "error")
        return redirect(url_for("recipes.list_recipes"))

    recipe_model.delete(recipe_id)
    flash("Receta eliminada.", "success")
    return redirect(url_for("recipes.list_recipes"))
