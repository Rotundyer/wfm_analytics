from uuid import UUID

from typing import Union
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from db.models import PartOfSet
from db.models import Item


# Класс для работы с таблицой с связями между предметами в БД
class PartOfSetDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # Создание связи
    async def create_part_of_set(self,
                                 item_id: UUID,
                                 part_id: UUID,
                                 main_name: str = None,
                                 part_name: str = None) -> PartOfSet:
        new_part_of_set = PartOfSet(
            item_id=item_id,
            part_id=part_id,
            main_name=main_name,
            part_name=part_name
        )
        # Проверка на дубликат
        query = select(PartOfSet).where(PartOfSet.item_id == item_id, PartOfSet.part_id == part_id)
        res = await self.db_session.execute(query)
        row = res.fetchone()
        if row is None:
            self.db_session.add(new_part_of_set)
            await self.db_session.flush()
        else:
            print(f'{item_id} is already linked with {part_id} in PartOfSet table')
        return new_part_of_set

    # Создание связи на основе 2 наименований
    async def create_part_of_set_with_str(self, main_name: str, part_name: str) -> Union[PartOfSet, None]:
        # Получение UUID первого предмета
        query = select(Item).where(Item.url_name == main_name)
        res = await self.db_session.execute(query)
        row = res.fetchone()
        if row is None:
            return None
        item_id = row[0].item_id

        # Получение UUID второго предмета
        query = select(Item).where(Item.url_name == part_name)
        res = await self.db_session.execute(query)
        row = res.fetchone()
        if row is None:
            return None
        part_id = row[0].item_id

        # Создание связи
        new_part_of_set = PartOfSet(
            item_id=item_id,
            part_id=part_id,
            main_name=main_name,
            part_name=part_name
        )
        self.db_session.add(new_part_of_set)
        await self.db_session.flush()
        return new_part_of_set
