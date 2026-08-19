# Mi Receta App

Aplicación web de recetas de cocina construida en Python con **Flask**, **SQLite** y arquitectura **MVC**. El entorno y las dependencias se gestionan con [`uv`](https://docs.astral.sh/uv/).

## Estructura del proyecto

```
app/
├── models/         # Modelo: acceso a datos (SQLite)
├── controllers/    # Controlador: rutas Flask (Blueprints)
└── views/          # Vista: templates Jinja2 + estáticos
schema.sql          # Definición de las tablas `recipes` y `categories`
run.py              # Punto de entrada de la aplicación
```

## Requisitos

- [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado.

## Instalación

```bash
uv sync
```

Esto crea el entorno virtual (`.venv/`) e instala las dependencias definidas en `pyproject.toml`.

## Ejecutar los tests

```bash
uv run pytest
```

## Ejecutar la aplicación

```bash
uv run run.py
```

O usando el CLI de Flask:

```bash
uv run flask --app run run --debug
```

La app estará disponible en http://127.0.0.1:5000. Al arrancar se crea automáticamente la base de datos SQLite en `instance/recetas.db`.

## Cargar recetas de ejemplo

```bash
uv run python scripts/seed_desserts.py
uv run python scripts/seed_meats.py
```

- `seed_desserts.py`: 4 recetas de postres (flan de coco, queque de chocolate, torta de melocotón, suspiro limeño) en la categoría "Postres".
- `seed_meats.py`: 3 recetas de carnes (lomo saltado, costillas de cerdo a la barbacoa, pollo a la brasa) en la categoría "Platos fuertes".

Ambos scripts incluyen ingredientes, pasos detallados e ilustración por receta.

## Funcionalidades

- Listar recetas, con filtro opcional por categoría
- Ver el detalle de una receta
- Crear, editar y eliminar recetas
- Asignar una categoría (opcional) e imagen (opcional) a cada receta
- Crear, listar, editar y eliminar categorías (al eliminar una categoría, las recetas asociadas quedan sin categoría)
