def test_list_categories_empty(client):
    response = client.get("/categorias")
    assert response.status_code == 200
    assert "primera".encode() in response.data


def test_create_category(client):
    response = client.post("/categorias/nueva", data={"name": "Postres"})
    assert response.status_code == 302

    listing = client.get("/categorias")
    assert b"Postres" in listing.data


def test_create_category_missing_name(client):
    response = client.post("/categorias/nueva", data={"name": ""})
    assert response.status_code == 400
    assert "obligatorio".encode() in response.data


def test_create_category_duplicate_name(client):
    client.post("/categorias/nueva", data={"name": "Postres"})
    response = client.post("/categorias/nueva", data={"name": "postres"})
    assert response.status_code == 400
    assert "Ya existe".encode() in response.data


def test_edit_category(client):
    client.post("/categorias/nueva", data={"name": "Postres"})
    response = client.post("/categorias/1/editar", data={"name": "Postres y dulces"})
    assert response.status_code == 302

    listing = client.get("/categorias")
    assert b"Postres y dulces" in listing.data


def test_delete_category(client):
    client.post("/categorias/nueva", data={"name": "Postres"})
    response = client.post("/categorias/1/eliminar")
    assert response.status_code == 302

    listing = client.get("/categorias")
    assert "primera".encode() in listing.data
