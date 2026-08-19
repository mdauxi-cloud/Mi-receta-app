"""Carga 3 recetas de carnes (lomo saltado, costillas de cerdo a la
barbacoa y pollo a la brasa) en la categoría "Platos fuertes".

Uso: uv run python scripts/seed_meats.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.models import category as category_model
from app.models import recipe as recipe_model

MEATS = [
    {
        "title": "Lomo saltado",
        "description": (
            "Salteado peruano de tiras de lomo con cebolla, tomate y papas "
            "fritas, a fuego alto y en pocos minutos. Sabor intenso y jugoso."
        ),
        "ingredients": "\n".join(
            [
                "600 g de lomo de res, en tiras",
                "2 papas grandes, en bastones y fritas",
                "1 cebolla roja, en gajos gruesos",
                "2 tomates, en gajos",
                "2 dientes de ajo, picados",
                "1 ají amarillo, en tiras (sin venas ni semillas)",
                "3 cucharadas de sillao (salsa de soya)",
                "1 cucharada de vinagre tinto",
                "1/2 cucharadita de comino",
                "Aceite vegetal",
                "Sal y pimienta al gusto",
                "Cilantro fresco picado, para decorar",
                "Arroz blanco cocido, para acompañar",
            ]
        ),
        "steps": "\n".join(
            [
                "Sazona las tiras de lomo con sal, pimienta y comino.",
                "Fríe las papas en bastones hasta que estén doradas y crocantes; resérvalas.",
                "Calienta un wok o sartén grande a fuego muy alto con un chorro de aceite.",
                "Sella la carne en tandas pequeñas (para que no suelte agua), solo 1-2 minutos por tanda, y retira.",
                "En el mismo wok, saltea el ajo unos segundos, añade la cebolla y el ají amarillo a fuego alto por 1 minuto.",
                "Incorpora el tomate y saltea 1 minuto más, sin que se deshaga del todo.",
                "Regresa la carne al wok, añade el sillao y el vinagre, y saltea todo junto 1-2 minutos.",
                "Agrega las papas fritas al final y mezcla rápidamente para que se impregnen del jugo sin perder el crocante.",
                "Espolvorea cilantro picado y sirve de inmediato acompañado de arroz blanco.",
            ]
        ),
        "prep_time_minutes": 20,
        "cook_time_minutes": 15,
        "servings": 4,
        "image_filename": "img/meats/lomo-saltado.svg",
    },
    {
        "title": "Costillas de cerdo a la barbacoa",
        "description": (
            "Costillar de cerdo cocido lento hasta quedar tierno, glaseado con "
            "salsa barbacoa caramelizada. Nivel restaurante, hecho en casa."
        ),
        "ingredients": "\n".join(
            [
                "1 costillar de cerdo (aprox. 1.5 kg)",
                "2 cucharadas de azúcar rubia",
                "1 cucharada de pimentón (paprika)",
                "1 cucharadita de ajo en polvo",
                "1 cucharadita de cebolla en polvo",
                "1 cucharadita de sal",
                "1/2 cucharadita de pimienta negra",
                "1/2 cucharadita de comino",
                "200 ml de salsa barbacoa",
                "2 cucharadas de vinagre de manzana",
            ]
        ),
        "steps": "\n".join(
            [
                "Retira la membrana plateada del dorso del costillar para que quede más tierno.",
                "Mezcla el azúcar, pimentón, ajo en polvo, cebolla en polvo, sal, pimienta y comino para preparar el rub seco.",
                "Frota el rub por ambos lados del costillar y déjalo reposar en refrigeración al menos 2 horas (idealmente toda la noche).",
                "Precalienta el horno a 150 °C.",
                "Envuelve el costillar en papel aluminio y hornea entre 2.5 y 3 horas, hasta que la carne esté muy tierna.",
                "Retira del horno, desenvuelve y mezcla la salsa barbacoa con el vinagre de manzana; pincela generosamente el costillar por ambos lados.",
                "Sube la temperatura del horno a 220 °C (o usa la parrilla/grill) y hornea 10-15 minutos más, hasta que la salsa caramelice.",
                "Deja reposar 5 minutos, corta entre hueso y hueso, y sirve con más salsa barbacoa aparte.",
            ]
        ),
        "prep_time_minutes": 20,
        "cook_time_minutes": 180,
        "servings": 4,
        "image_filename": "img/meats/costillas-bbq.svg",
    },
    {
        "title": "Pollo a la brasa",
        "description": (
            "Pollo entero marinado con especias peruanas y asado hasta lograr "
            "una piel dorada y crocante por fuera, jugosa por dentro."
        ),
        "ingredients": "\n".join(
            [
                "1 pollo entero (aprox. 1.8 kg)",
                "4 dientes de ajo molidos",
                "2 cucharadas de sillao (salsa de soya)",
                "2 cucharadas de pasta de ají panca",
                "1 cucharada de comino",
                "1 cucharada de pimentón (paprika)",
                "1 cucharadita de orégano seco",
                "1/2 taza de cerveza o pisco",
                "2 cucharadas de aceite vegetal",
                "Sal y pimienta al gusto",
                "2 cucharadas de mantequilla derretida, para bañar",
            ]
        ),
        "steps": "\n".join(
            [
                "Mezcla el ajo, sillao, ají panca, comino, pimentón, orégano, cerveza, aceite, sal y pimienta para formar el marinado.",
                "Frota el pollo por dentro y por fuera con el marinado, incluso debajo de la piel de la pechuga.",
                "Cubre y refrigera al menos 4 horas, idealmente toda la noche.",
                "Precalienta el horno a 220 °C. Bridea el pollo (amarra las patas) para una cocción pareja.",
                "Coloca el pollo con la pechuga hacia arriba sobre una rejilla y hornea 20 minutos para dorar la piel.",
                "Baja la temperatura a 190 °C y sigue horneando 50-60 minutos más, bañando con la mantequilla derretida cada 20 minutos.",
                "Verifica que esté cocido (jugos claros al pinchar el muslo o 74 °C internos) y deja reposar 10 minutos antes de trinchar.",
                "Sirve con papas fritas, ensalada y salsa de ají o crema huancaína.",
            ]
        ),
        "prep_time_minutes": 30,
        "cook_time_minutes": 90,
        "servings": 5,
        "image_filename": "img/meats/pollo-brasa.svg",
    },
]


def main():
    app = create_app()
    with app.app_context():
        category = next(
            (c for c in category_model.get_all() if c["name"] == "Platos fuertes"),
            None,
        )
        category_id = (
            category["id"] if category else category_model.create("Platos fuertes")
        )

        created = 0
        for meat in MEATS:
            existing = next(
                (r for r in recipe_model.get_all() if r["title"] == meat["title"]),
                None,
            )
            if existing:
                print(f"Ya existe, se omite: {meat['title']}")
                continue

            data = dict(meat)
            data["category_id"] = category_id
            recipe_model.create(data)
            created += 1
            print(f"Receta creada: {meat['title']}")

        print(f"\nListo. {created} receta(s) nueva(s) en la categoría 'Platos fuertes'.")


if __name__ == "__main__":
    main()
