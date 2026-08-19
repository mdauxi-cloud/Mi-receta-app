# Mi Receta App

Aplicación web de recetas de cocina construida en Python con **Flask**, **SQLite** y arquitectura **MVC**. El entorno y las dependencias se gestionan con [`uv`](https://docs.astral.sh/uv/).

## Estructura del proyecto

```
app/
├── models/         # Modelo: acceso a datos (SQLite)
├── controllers/    # Controlador: rutas Flask (Blueprints)
└── views/          # Vista: templates Jinja2 + estáticos
schema.sql          # Definición de la tabla `recipes`
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

## Funcionalidades (v1)

- Listar recetas
- Ver el detalle de una receta
- Crear una receta nueva
- Editar una receta existente
- Eliminar una receta
