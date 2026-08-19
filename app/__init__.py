from pathlib import Path

from flask import Flask, redirect, url_for

from app.models import database


def create_app(test_config=None):
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="views/templates",
        static_folder="views/static",
    )
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=str(Path(app.instance_path) / "recetas.db"),
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,
    )

    if test_config is not None:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    (Path(app.static_folder) / "uploads").mkdir(parents=True, exist_ok=True)

    database.init_app(app)

    if not Path(app.config["DATABASE"]).exists():
        with app.app_context():
            database.init_db()

    from app.controllers.category_controller import categories_bp
    from app.controllers.recipe_controller import recipes_bp

    app.register_blueprint(recipes_bp)
    app.register_blueprint(categories_bp)

    @app.get("/")
    def index():
        return redirect(url_for("recipes.list_recipes"))

    return app
