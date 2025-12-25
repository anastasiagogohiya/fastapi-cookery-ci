"""Модели БД"""

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class RecipesData(Base):
    __tablename__ = "recipes_data"

    recipe_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )  # noqa: E501
    dish_name: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
    )  # уникальное название блюд
    cooking_time_minutes: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )  # в минутах.
    ingredients: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    views_count: Mapped[int] = mapped_column(
        Integer, default=0, index=True
    )  # по умолчанию 0 просмотров
