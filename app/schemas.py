from pydantic import BaseModel, Field


class GetAllRecipes(BaseModel):
    """Поля вывода общей информации по всем рецептам"""

    recipe_id: int
    dish_name: str
    views_count: int
    cooking_time_minutes: int


class GetRecipeId(BaseModel):
    """Поля вывода подробных данных по ID рецепта"""

    recipe_id: int
    dish_name: str
    cooking_time_minutes: int
    ingredients: str
    description: str


class AddRecipe(BaseModel):
    """Поля для добавления нового рецепта (подробные данные)"""

    dish_name: str = Field(description="Название блюда", examples=["Чашушули"])

    cooking_time_minutes: int = Field(
        description="Время приготовления в минутах", examples=[60]
    )

    ingredients: str = Field(
        description="Перечисление ингредиентов для приготовления и граммовки",
        examples=["Говядина: 800г, растит. масло: 1 ст. ложка, томаты: 300г"],
    )

    description: str = Field(
        description="Описание блюда",
        examples=[
            "Тушёное мясо кусочками с томатами, " "луком, болгарским перцем"
        ],  # noqa: E501
    )
