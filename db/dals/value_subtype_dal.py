from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from db.models import ValueSubtype
from api.models import Subtype as ShowSubtype


# Класс для работы с таблицой со списком уникальных _ПОБОЧНЫХ_ тэгов в БД
class ValueSubtypeDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # Создание _ПОБОЧНОГО_ уникального тэга
    async def create_value_subtype(self, subtype: str) -> ValueSubtype:
        query = select(ValueSubtype).where(ValueSubtype.subtype == subtype)
        res = await self.db_session.execute(query)
        row = res.fetchone()
        new_value_subtype = ValueSubtype(subtype=subtype)
        if row is None:
            self.db_session.add(new_value_subtype)
            await self.db_session.flush()
        else:
            print(f'{subtype} is already in the Value Subtype table')
        return new_value_subtype

    # Получение списка всех уникальных _ПОБОЧНЫХ_ тэгов
    async def get_all_subtypes(self) -> list[ShowSubtype]:
        subtypes: list[ShowSubtype] = []
        query = select(ValueSubtype)
        res = await self.db_session.execute(query)
        rows = res.fetchall()
        if rows is not None:
            for row in rows:
                subtypes.append(ShowSubtype(id=row[0].id, subtype=row[0].subtype))
        return subtypes
