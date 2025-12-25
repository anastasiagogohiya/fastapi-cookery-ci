import re
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_async_session, init_db
from .models import RecipesData
from .schemas import AddRecipe, GetAllRecipes, GetRecipeId

"""Код запуска приложения"""


"""На фоне: uvicorn app.app:app --reload,
url в браузере http://127.0.0.1:8000/
url для документации http://127.0.0.1:8000/docs"""


"""
Используем контекстный менеджер при старту и завершении работы приложения.
"""


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await init_db()  # создаем БД.
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Кулинарная книга с рецептами грузинской кухни",
    description="API для работы с рецептами грузинской кухни",
)  # инициализация приложения


@app.get(
    "/recipes",
    response_model=List[GetAllRecipes],
    tags=["Рецепты"],
    summary="Запрос списка рецептов с кол-вом просмотров.",
    description="Получение списка рецептов, "
    "отсортированных по популярности и времени приготовления.",
)
async def get_all_recipes(
    session: AsyncSession = Depends(get_async_session),  # noqa: B008
) -> list[RecipesData]:
    """Список рецептов: отсортированы по кол-ву просмотров
    — тому, сколько раз открыли детальный рецепт.
    Чем чаще открывают рецепт, тем он популярнее.
    Если число просмотров совпадает, рецепты сортируются по t приготовления.
    """
    result = await session.execute(
        select(RecipesData).order_by(
            desc(RecipesData.views_count),
            asc(RecipesData.cooking_time_minutes),  # noqa: E501
        )
    )

    return list(result.scalars().all())


@app.get(
    "/recipes/{recipe_id}",
    response_model=GetRecipeId,
    tags=["Рецепты"],
    summary="Запрос детальной информации по ID рецепта.",
    description="Получение детальной информации по ID, "
    "также увеличиваем счетчик +1 на просмотр.",
)  # одно значение
async def get_recipe_by_id(
    recipe_id: int,
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, E501
) -> RecipesData:
    """
    Детальная информация по рецепту по ID + инкремент просмотров
    """
    result = await session.execute(
        select(RecipesData).where(RecipesData.recipe_id == recipe_id)
    )
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    """Инкремент"""
    recipe.views_count += 1
    await session.commit()
    return recipe


@app.post(
    "/recipes",
    response_model=GetRecipeId,
    tags=["Рецепты"],
    summary="Запрос на добавление нового рецепта.",
    description="Добавляем в БД новый рецепт с заполненными полями.",
)
async def create_recipes(
    recipe: AddRecipe,
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, E501
) -> RecipesData:
    """
    Можно ввести новый рецепт.
    """
    new_recipe = RecipesData(**recipe.model_dump())
    session.add(new_recipe)  # добавляем новый рецепт в сессию
    await session.commit()  # сохраняем сессию
    await session.refresh(new_recipe)  # обновление данных
    return new_recipe


@app.get(
    "/recipes/search/{string}",
    response_model=list[GetAllRecipes],
    tags=["Рецепты"],
    summary="Запрос на поиск рецепта по совпадению введенному слову",
    description="Получаем рецепты по совпадениям из названий блюд и описанию блюд.",  # noqa: E501
)
async def find_recipes(
    string: str, session: AsyncSession = Depends(get_async_session)  # noqa: B008, E501
) -> list[RecipesData]:
    """
    Поиск рецепта по строке пользователя в названии блюда и описании.
    """

    s = string.strip()

    # Быстрый регистронезависимый SQL-поиск
    query = await session.execute(
        select(RecipesData).where(
            or_(
                func.lower(RecipesData.dish_name).like(f"%{s.lower()}%"),
                func.lower(RecipesData.description).like(f"%{s.lower()}%"),
            )
        )
    )
    interim_results: list[RecipesData] = list(query.scalars().all())

    # через re, так как не все результаты выше метод выводит!
    if len(interim_results) < 5:
        query2 = await session.execute(select(RecipesData))
        all_recipes: list[RecipesData] = list(query2.scalars().all())

        pattern = re.compile(re.escape(s), re.IGNORECASE)
        interim_results.extend(
            r
            for r in all_recipes
            if pattern.search(r.dish_name or "")
            or pattern.search(r.description or "")  # noqa: E501
        )

        results: list[RecipesData] = list(
            {r.recipe_id: r for r in interim_results}.values()
        )

    return list(results)
