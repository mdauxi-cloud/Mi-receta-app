"""Carga las 4 recetas de postres de ejemplo (flan de coco, queque de
chocolate, torta de melocotón y suspiro limeño) en la categoría "Postres".

Uso: uv run python scripts/seed_desserts.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.models import category as category_model
from app.models import recipe as recipe_model

DESSERTS = [
    {
        "title": "Flan de coco",
        "description": (
            "Flan cremoso de coco bañado en caramelo, cocido a baño María. "
            "Receta de nivel chef, textura sedosa garantizada."
        ),
        "ingredients": "\n".join(
            [
                "1 lata de leche condensada (395 g)",
                "1 lata de leche evaporada (410 ml)",
                "200 ml de leche de coco",
                "4 huevos",
                "1 yema de huevo adicional",
                "1 cucharadita de esencia de vainilla",
                "150 g de azúcar (para el caramelo)",
                "2 cucharadas de agua (para el caramelo)",
                "50 g de coco rallado, para decorar",
            ]
        ),
        "steps": "\n".join(
            [
                "Precalienta el horno a 160 °C.",
                "Prepara el caramelo: derrite el azúcar con el agua a fuego medio sin remover hasta lograr un color ámbar y viértelo de inmediato en el molde de flan, cubriendo el fondo.",
                "Licúa la leche condensada, la leche evaporada, la leche de coco, los huevos, la yema extra y la vainilla hasta obtener una mezcla homogénea.",
                "Cuela la mezcla sobre el molde acaramelado para eliminar grumos.",
                "Cubre el molde con papel aluminio y colócalo dentro de una bandeja con agua caliente hasta la mitad (baño María).",
                "Hornea entre 55 y 65 minutos, hasta que al insertar un cuchillo salga limpio.",
                "Deja enfriar a temperatura ambiente y luego refrigera al menos 4 horas (idealmente toda la noche).",
                "Pasa un cuchillo por los bordes, desmolda sobre un plato hondo y decora con coco rallado tostado.",
            ]
        ),
        "prep_time_minutes": 20,
        "cook_time_minutes": 60,
        "servings": 8,
        "image_filename": "img/desserts/flan-coco.svg",
    },
    {
        "title": "Queque de chocolate",
        "description": (
            "Bizcocho de chocolate esponjoso y húmedo, con cobertura brillante. "
            "Un clásico de repostería con acabado profesional."
        ),
        "ingredients": "\n".join(
            [
                "200 g de mantequilla a temperatura ambiente",
                "250 g de azúcar",
                "3 huevos",
                "250 g de harina",
                "60 g de cacao en polvo sin azúcar",
                "1 cucharada de polvo de hornear",
                "1/2 cucharadita de sal",
                "180 ml de leche",
                "1 cucharadita de esencia de vainilla",
                "100 g de chocolate negro, para la cobertura",
                "80 ml de crema de leche, para la cobertura",
            ]
        ),
        "steps": "\n".join(
            [
                "Precalienta el horno a 180 °C y engrasa un molde para queque.",
                "Bate la mantequilla con el azúcar hasta obtener una mezcla pálida y cremosa.",
                "Incorpora los huevos uno a uno, batiendo bien después de cada adición.",
                "Cierne juntos la harina, el cacao, el polvo de hornear y la sal.",
                "Añade los ingredientes secos a la mezcla alternando con la leche y la vainilla, comenzando y terminando con los secos.",
                "Vierte la mezcla en el molde y hornea entre 40 y 45 minutos, hasta que un palillo salga limpio.",
                "Deja enfriar 10 minutos en el molde y luego desmolda sobre una rejilla.",
                "Para la cobertura, calienta la crema de leche y viértela sobre el chocolate picado; deja reposar 2 minutos y mezcla hasta lograr un ganache brillante.",
                "Baña el queque frío con el ganache y deja que cuaje antes de servir.",
            ]
        ),
        "prep_time_minutes": 25,
        "cook_time_minutes": 45,
        "servings": 10,
        "image_filename": "img/desserts/queque-chocolate.svg",
    },
    {
        "title": "Torta de melocotón",
        "description": (
            "Bizcocho suave cubierto con melocotones jugosos y un toque de canela. "
            "Ligera, aromática y perfecta para acompañar con té."
        ),
        "ingredients": "\n".join(
            [
                "180 g de harina",
                "1 cucharadita de polvo de hornear",
                "1/4 cucharadita de sal",
                "120 g de mantequilla a temperatura ambiente",
                "150 g de azúcar",
                "2 huevos",
                "1 cucharadita de esencia de vainilla",
                "100 ml de leche",
                "4 melocotones maduros, en gajos (o 1 lata de melocotones en almíbar, escurridos)",
                "1 cucharadita de canela en polvo",
                "2 cucharadas de azúcar, para espolvorear",
            ]
        ),
        "steps": "\n".join(
            [
                "Precalienta el horno a 175 °C y engrasa un molde redondo desmontable.",
                "Cierne la harina con el polvo de hornear y la sal.",
                "Bate la mantequilla con el azúcar hasta que esté cremosa; añade los huevos uno a uno y luego la vainilla.",
                "Incorpora los secos alternando con la leche hasta lograr una masa lisa.",
                "Vierte la masa en el molde y acomoda los gajos de melocotón en forma de abanico sobre la superficie.",
                "Espolvorea con la canela y el azúcar restante.",
                "Hornea entre 40 y 50 minutos, hasta que esté dorada y un palillo salga limpio.",
                "Deja enfriar en el molde 15 minutos antes de desmoldar y servir.",
            ]
        ),
        "prep_time_minutes": 20,
        "cook_time_minutes": 45,
        "servings": 8,
        "image_filename": "img/desserts/torta-melocoton.svg",
    },
    {
        "title": "Suspiro limeño",
        "description": (
            "Postre bandera del Perú: base de manjar blanco cubierta con un "
            "delicado merengue al oporto y un toque de canela. Elegancia en copa."
        ),
        "ingredients": "\n".join(
            [
                "1 lata de leche evaporada (410 ml)",
                "1 lata de leche condensada (395 g)",
                "3 yemas de huevo",
                "1 cucharadita de esencia de vainilla",
                "3 claras de huevo",
                "150 g de azúcar",
                "60 ml de agua",
                "50 ml de oporto (vino dulce)",
                "Canela en polvo, para decorar",
            ]
        ),
        "steps": "\n".join(
            [
                "En una olla, mezcla la leche evaporada con la leche condensada y cocina a fuego medio, removiendo constantemente.",
                "Cuando espese ligeramente, retira un poco de la mezcla caliente y bátela con las yemas para temperarlas; regresa todo a la olla.",
                "Sigue cociendo a fuego bajo, sin dejar de remover, hasta obtener una consistencia de manjar blanco espeso (10-15 minutos). Añade la vainilla y retira del fuego.",
                "Reparte el manjar en copas individuales y refrigera al menos 1 hora.",
                "Para el merengue, hierve el azúcar con el agua hasta formar un almíbar a punto de hilo fuerte (aprox. 115 °C).",
                "Bate las claras a punto de nieve y vierte el almíbar caliente en hilo fino sin dejar de batir, hasta lograr un merengue italiano brillante y firme.",
                "Incorpora el oporto al merengue con movimientos envolventes.",
                "Cubre cada copa de manjar con el merengue, usando manga pastelera para un acabado prolijo.",
                "Espolvorea con canela justo antes de servir.",
            ]
        ),
        "prep_time_minutes": 30,
        "cook_time_minutes": 25,
        "servings": 6,
        "image_filename": "img/desserts/suspiro-limeno.svg",
    },
]


def main():
    app = create_app()
    with app.app_context():
        category = next(
            (c for c in category_model.get_all() if c["name"] == "Postres"), None
        )
        category_id = category["id"] if category else category_model.create("Postres")

        created = 0
        for dessert in DESSERTS:
            existing = next(
                (r for r in recipe_model.get_all() if r["title"] == dessert["title"]),
                None,
            )
            if existing:
                print(f"Ya existe, se omite: {dessert['title']}")
                continue

            data = dict(dessert)
            data["category_id"] = category_id
            recipe_model.create(data)
            created += 1
            print(f"Receta creada: {dessert['title']}")

        print(f"\nListo. {created} receta(s) nueva(s) en la categoría 'Postres'.")


if __name__ == "__main__":
    main()
