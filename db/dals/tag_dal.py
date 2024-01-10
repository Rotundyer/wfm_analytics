from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession

from db.models import Tag


# Класс для работы с таблицой с _ОСНОВНЫМИ_ тегами, связанными с предметами в БД
class TagDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # Создание _ОСНОВНОГО_ тега и его связи с предметом
    async def create_tag(self, item_id: UUID, tag: str) -> Tag:
        #
        # TODO: добавить обработку дубликатов
        #
        new_tag = Tag(
            item_id=item_id,
            tag=tag
        )
        self.db_session.add(new_tag)
        await self.db_session.flush()
        return new_tag
