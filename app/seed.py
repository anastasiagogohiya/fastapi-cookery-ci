import asyncio

from sqlalchemy import delete

from .db import async_session
from .models import RecipesData

"""Файл для заполнения базы данных для первого запуска. Код запускается отсюда.
10 грузинских блюд, формат JSON."""

RECIPES_DATA = [
    {
        "dish_name": "Хачапури по-аджарски",
        "cooking_time_minutes": 45,
        "ingredients": "мука: 500г, "
        "сыр сулугуни: 400г, "
        "яйцо: 2шт, "
        "масло сливочное: 50г",
        "description": "Лодочка из теста с сыром и яйцом сверху.",
        "views_count": 450,
    },
    {
        "dish_name": "Хинкали",
        "cooking_time_minutes": 60,
        "ingredients": "мясной фарш: 1кг, лук: 200г, кизма: 1ч.л., тесто: 1кг",
        "description": "Сочные мясные пельмени с хвостиком.",
        "views_count": 500,
    },
    {
        "dish_name": "Чахохбили",
        "cooking_time_minutes": 50,
        "ingredients": "курица: 1кг, "
        "помидоры: 800г, "
        "лук: 300г, "
        "хмели-сунели: 2ст.л.",
        "description": "Тушеная курица в томатном соусе.",
        "views_count": 300,
    },
    {
        "dish_name": "Сациви",
        "cooking_time_minutes": 120,
        "ingredients": "курица: 1.5кг, "
        "орехи грецкие: 300г, "
        "чеснок: 4зуб., "
        "хмели-сунели: 2ст.л.",
        "description": "Курица в ореховом соусе.",
        "views_count": 350,
    },
    {
        "dish_name": "Лобио",
        "cooking_time_minutes": 90,
        "ingredients": "фасоль красная: 500г, "
        "орехи: 100г, "
        "лук: 150г, "
        "коряндр: пучок",
        "description": "Густая фасолевая похлебка с орехами.",
        "views_count": 300,
    },
    {
        "dish_name": "Шашлык по-грузински",
        "cooking_time_minutes": 40,
        "ingredients": "свинина: 1.5кг, "
        "лук: 500г, "
        "вино красное: 200мл, "
        "хмели-сунели: 2ст.л.",
        "description": "Маринованный шашлык на мангале.",
        "views_count": 320,
    },
    {
        "dish_name": "Аджапсандали",
        "cooking_time_minutes": 60,
        "ingredients": "баклажаны: 500г, "
        "перец болг.: 400г, "
        "помидоры: 500г, "
        "чеснок: 5зуб.",
        "description": "Овощное рагу баклажанов и перца.",
        "views_count": 250,
    },
    {
        "dish_name": "Ткемали",
        "cooking_time_minutes": 30,
        "ingredients": "сливы терн: 1кг, "
        "чеснок: 5зуб., "
        "коряндр: 1ч.л., "
        "укроп: пучок",
        "description": "Кислый соус из слив.",
        "views_count": 350,
    },
    {
        "dish_name": "Мцвади",
        "cooking_time_minutes": 35,
        "ingredients": "говядина: 1кг, "
        "сало: 100г, "
        "соль: по вкусу, "
        "перец: по вкусу",
        "description": "Простой мясной шашлык.",
        "views_count": 250,
    },
    {
        "dish_name": "Пхали из шпината",
        "cooking_time_minutes": 25,
        "ingredients": "шпинат: 600г, "
        "орехи: 150г, "
        "чеснок: 3зуб., "
        "грецкие орехи: 100г",
        "description": "Ореховая паста из зелени.",
        "views_count": 100,
    },
]


"""Массовая загрузка в БД."""


async def seed_db() -> None:
    async with async_session() as session:
        """Очистка данных БД"""
        await session.execute(delete(RecipesData))
        await session.commit()
        print("БД очищена!")

        """Перезалив"""
        session.add_all([RecipesData(**data) for data in RECIPES_DATA])
        await session.commit()
        print("БД загружена!")


if __name__ == "__main__":
    asyncio.run(seed_db())
