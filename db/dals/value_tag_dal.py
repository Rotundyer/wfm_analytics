from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from db.models import ValueTag
from api.models import Tag as ShowTag


# Класс для работы с таблицой со списком уникальных _ОСНОВНЫХ_ тэгов в БД
class ValueTagDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # Создание _ОСНОВНОГО_ уникального тэга
    async def create_value_tag(self, tag: str) -> ValueTag:
        query = select(ValueTag).where(ValueTag.tag == tag)
        res = await self.db_session.execute(query)
        row = res.fetchone()
        new_value_tag = ValueTag(tag=tag)
        if row is None:
            self.db_session.add(new_value_tag)
            await self.db_session.flush()
        else:
            print(f'{tag} is already in the Value Tag table')
        return new_value_tag

    # Получение списка всех уникальных _ОСНОВНЫХ_ тэгов
    async def get_all_value_tags(self) -> list[ShowTag]:
        tags: list[ShowTag] = []
        query = select(ValueTag)
        res = await self.db_session.execute(query)
        rows = res.fetchall()
        if rows is not None:
            for row in rows:
                tags.append(ShowTag(id=row[0].id, tag=row[0].tag))
        return tags
