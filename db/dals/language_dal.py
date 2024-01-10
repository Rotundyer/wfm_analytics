import uuid

from sqlalchemy.ext.asyncio.session import AsyncSession

from db.models import Language


# Класс для работы с таблицой с локализациями в БД
class LanguageDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # Создание локализации
    async def create_language(self,
                              item_id: uuid.UUID,
                              item_name: str,
                              language: str,
                              description: str = None,
                              wiki_link: str = None) -> Language:
        new_language = Language(
            item_id=item_id,
            language=language,
            item_name=item_name,
            description=description,
            wiki_link=wiki_link
        )
        #
        # TODO: добавить обработку дубликатов
        #
        self.db_session.add(new_language)
        await self.db_session.flush()
        return new_language
