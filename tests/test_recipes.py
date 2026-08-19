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
