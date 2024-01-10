from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession

from db.models import Subtype


# Класс для работы с таблицой с _ПОБОЧНЫМИ_ тегами, связанными с предметами в БД
class SubtypeDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # Создание _ПОБОЧНОГО_ тега и его связи с предметом
    async def create_subtype(self, item_id: UUID, subtype: str) -> Subtype:
        #
        # TODO: добавить обработку дубликатов
        #
        new_subtype = Subtype(
            item_id=item_id,
            subtype=subtype
        )
        self.db_session.add(new_subtype)
        await self.db_session.flush()
        return new_subtype
