from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models import category as category_model

categories_bp = Blueprint("categories", __name__, url_prefix="/categorias")


def _parse_form(form, exclude_id=None):
    errors = {}

    name = form.get("name", "").strip()
    if not name:
        errors["name"] = "El nombre es obligatorio."
    elif category_model.name_exists(name, exclude_id=exclude_id):
        errors["name"] = "Ya existe una categoría con ese nombre."

    return {"name": name}, errors


@categories_bp.get("")
def list_categories():
    categories = category_model.get_all()
    return render_template("categories/list.html", categories=categories)


@categories_bp.get("/nueva")
def new_category():
    return render_template("categories/form.html", category=None, errors={})


@categories_bp.post("/nueva")
def create_category():
    data, errors = _parse_form(request.form)
    if errors:
        return render_template("categories/form.html", category=data, errors=errors), 400

    category_model.create(data["name"])
    flash("Categoría creada correctamente.", "success")
    return redirect(url_for("categories.list_categories"))


@categories_bp.get("/<int:category_id>/editar")
def edit_category(category_id):
    category = category_model.get_by_id(category_id)
    if category is None:
        flash("La categoría solicitada no existe.", "error")
        return redirect(url_for("categories.list_categories"))
    return render_template("categories/form.html", category=category, errors={})


@categories_bp.post("/<int:category_id>/editar")
def update_category(category_id):
    if category_model.get_by_id(category_id) is None:
        flash("La categoría solicitada no existe.", "error")
        return redirect(url_for("categories.list_categories"))

    data, errors = _parse_form(request.form, exclude_id=category_id)
    if errors:
        data["id"] = category_id
        return render_template("categories/form.html", category=data, errors=errors), 400

    category_model.update(category_id, data["name"])
    flash("Categoría actualizada correctamente.", "success")
    return redirect(url_for("categories.list_categories"))


@categories_bp.post("/<int:category_id>/eliminar")
def delete_category(category_id):
    if category_model.get_by_id(category_id) is None:
        flash("La categoría solicitada no existe.", "error")
        return redirect(url_for("categories.list_categories"))

    category_model.delete(category_id)
    flash("Categoría eliminada.", "success")
    return redirect(url_for("categories.list_categories"))
