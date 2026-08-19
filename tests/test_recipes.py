VALID_RECIPE = {
    "title": "Tortilla de patatas",
    "description": "Clásico español",
    "ingredients": "Patatas\nHuevos\nAceite\nSal",
    "steps": "Pelar y cortar las patatas\nFreír las patatas\nBatir los huevos\nCuajar la tortilla",
    "prep_time_minutes": "15",
    "cook_time_minutes": "20",
    "servings": "4",
}


def test_index_redirects_to_list(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"] == "/recetas"


def test_list_empty(client):
    response = client.get("/recetas")
    assert response.status_code == 200
    assert "primera".encode() in response.data


def test_create_recipe_valid(client):
    response = client.post("/recetas/nueva", data=VALID_RECIPE, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "/recetas/1"

    detail = client.get("/recetas/1")
    assert detail.status_code == 200
    assert b"Tortilla de patatas" in detail.data


def test_create_recipe_missing_title(client):
    data = dict(VALID_RECIPE)
    data["title"] = ""
    response = client.post("/recetas/nueva", data=data)
    assert response.status_code == 400
    assert "obligatorio".encode() in response.data


def test_create_recipe_invalid_number(client):
    data = dict(VALID_RECIPE)
    data["servings"] = "abc"
    response = client.post("/recetas/nueva", data=data)
    assert response.status_code == 400
    assert "entero".encode() in response.data


def test_detail_not_found_redirects(client):
    response = client.get("/recetas/999", follow_redirects=True)
    assert response.status_code == 200
    assert "no existe".encode() in response.data


def test_edit_recipe(client):
    client.post("/recetas/nueva", data=VALID_RECIPE)

    updated = dict(VALID_RECIPE)
    updated["title"] = "Tortilla de patatas con cebolla"
    response = client.post("/recetas/1/editar", data=updated, follow_redirects=False)
    assert response.status_code == 302

    detail = client.get("/recetas/1")
    assert b"con cebolla" in detail.data


def test_delete_recipe(client):
    client.post("/recetas/nueva", data=VALID_RECIPE)

    response = client.post("/recetas/1/eliminar", follow_redirects=False)
    assert response.status_code == 302

    detail = client.get("/recetas/1", follow_redirects=True)
    assert "no existe".encode() in detail.data


def test_create_recipe_with_category(client):
    client.post("/categorias/nueva", data={"name": "Postres"})

    data = dict(VALID_RECIPE)
    data["category_id"] = "1"
    client.post("/recetas/nueva", data=data)

    detail = client.get("/recetas/1")
    assert b"Postres" in detail.data


def test_create_recipe_invalid_category(client):
    data = dict(VALID_RECIPE)
    data["category_id"] = "999"
    response = client.post("/recetas/nueva", data=data)
    assert response.status_code == 400
    assert "no existe".encode() in response.data


def test_filter_recipes_by_category(client):
    client.post("/categorias/nueva", data={"name": "Postres"})
    client.post("/categorias/nueva", data={"name": "Bebidas"})

    with_category = dict(VALID_RECIPE)
    with_category["category_id"] = "1"
    client.post("/recetas/nueva", data=with_category)

    without_category = dict(VALID_RECIPE)
    without_category["title"] = "Zumo de naranja"
    client.post("/recetas/nueva", data=without_category)

    response = client.get("/recetas?category_id=1")
    assert b"Tortilla de patatas" in response.data
    assert b"Zumo de naranja" not in response.data

    response = client.get("/recetas?category_id=2")
    assert b"Tortilla de patatas" not in response.data

    response = client.get("/recetas")
    assert b"Tortilla de patatas" in response.data
    assert b"Zumo de naranja" in response.data


def test_deleting_category_keeps_recipe(client):
    client.post("/categorias/nueva", data={"name": "Postres"})
    data = dict(VALID_RECIPE)
    data["category_id"] = "1"
    client.post("/recetas/nueva", data=data)

    client.post("/categorias/1/eliminar")

    detail = client.get("/recetas/1")
    assert detail.status_code == 200
    assert b"Tortilla de patatas" in detail.data
