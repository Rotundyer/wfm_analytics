from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import settings

# Модуль с сессией для работы с БД

# Создание движка
engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)

# Создание асинхронной сессии
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Функция для вызовов сессии
async def get_db() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
