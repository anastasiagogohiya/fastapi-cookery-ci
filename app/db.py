"""Асинхронное подключение к БД Cookery (Кулинария)"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (  # noqa: E501
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .models import Base

"""Название БД Cookery.db и сохранение в текущую директорию."""
DATABASE_NAME = "sqlite+aiosqlite:///./Cookery.db"

"""Создание асинхронного движка (пул соединений),
включаем логирование в общую консоль."""
engine = create_async_engine(DATABASE_NAME, echo=True)

"""Создание фабрики асинхронных сессий."""
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,  # noqa: E501, type: ignore[call-overload]
)

"""Создание конкретной асинхронной сессии."""


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для fastAPI, которая создает асинхронную сессию,
    передает ее в эндпоинты и закрывает сессию автоматически
    (Не нужно ее закрывать каждый раз!).
    """
    async with async_session() as session:
        yield session


async def init_db() -> None:
    """Берем одно соединение из асинхронного пула соединений"""
    async with engine.begin() as conn:
        """Создаем таблицы по моделям"""
        await conn.run_sync(Base.metadata.create_all)
