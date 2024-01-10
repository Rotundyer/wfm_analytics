from uuid import UUID
from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals.value_tag_dal import ValueTagDAL
from db.dals.value_subtype_dal import ValueSubtypeDAL
from db.dals.item_dal import ItemDAL

from api.models import Tag as ShowTag
from api.models import Subtype as ShowSubtype
from api.models import Item as ShowItem

from api.models import GetItems

from db.session import get_db

local_router = APIRouter()


# Получение списка _ОСНОВНЫХ_ тэгов
@local_router.get('/tags', response_model=list[ShowTag])
async def get_all_tags(db: AsyncSession = Depends(get_db)) -> list[ShowTag]:
    # Создание сессии для работы с БД
    async with db as session:
        async with session.begin():
            value_tag_dal = ValueTagDAL(session)
            return await value_tag_dal.get_all_value_tags()


# Получение списка _ПОБОЧНЫХ_ тэгов
@local_router.get('/subtypes', response_model=list[ShowSubtype])
async def get_all_subtypes(db: AsyncSession = Depends(get_db)) -> list[ShowSubtype]:
    # Создание сессии для работы с БД
    async with db as session:
        async with session.begin():
            value_subtype_dal = ValueSubtypeDAL(session)
            return await value_subtype_dal.get_all_subtypes()


# Получение информации по конкретному предмету
# Из необходимых данных: его UUID, ID из wfm или URL имени. Достаточно 1 параметра для поиска
# Из необязательных, но которые выводят дополнительную информацию о предмете:
# - _ОСНОВНЫЕ_ тэги предмета; _ПОБОЧНЫЕ_ теги предмета; взаимосвязи с другими предметами; локализации (одна конкретная или сразу все)
@local_router.get('/item', response_model=Union[ShowItem, str], response_model_exclude_defaults=True)
async def get_item(item_id: UUID = None,
                   url_name: str = None,
                   wfm_id: str = None,
                   is_tags: bool = False,
                   is_subtypes: bool = False,
                   is_parts: bool = False,
                   localization: str = None,
                   db: AsyncSession = Depends(get_db)) -> Union[ShowItem, str]:
    # Создание сессии для работы с БД
    async with db as session:
        async with session.begin():
            item_dal = ItemDAL(session)
            return await item_dal.get_item(item_id=item_id,
                                           url_name=url_name,
                                           wfm_id=wfm_id,
                                           is_tags=is_tags,
                                           is_subtypes=is_subtypes,
                                           is_parts=is_parts,
                                           localization=localization)


# Получение информации из передаваемых списков с индефекаторами
# Списки собирательные. Параметры получения информации такие же, как и у одиночного запроса
@local_router.get('/items', response_model=Union[list[ShowItem], str], response_model_exclude_defaults=True)
async def get_items(body: GetItems = None,
                    is_tags: bool = False,
                    is_subtypes: bool = False,
                    is_parts: bool = False,
                    localization: str = None,
                    db: AsyncSession = Depends(get_db)) -> Union[list[ShowItem], str]:
    async with db as session:
        async with session.begin():
            item_dal = ItemDAL(session)
            if body is None:
                return "Search parameters not set"
            return await item_dal.get_items(items_id=body.items_id,
                                            wfms_id=body.wfms_id,
                                            urls_name=body.urls_name,
                                            is_tags=is_tags,
                                            is_subtypes=is_subtypes,
                                            is_parts=is_parts,
                                            localization=localization)


# Получение списка предметов с параметром в виде _ОСНОВНОГО_ тега
@local_router.get('/items/tag', response_model=Union[list[ShowItem], str], response_model_exclude_defaults=True)
async def get_items_from_tag(tag: str,
                             is_tags: bool = False,
                             is_subtypes: bool = False,
                             is_parts: bool = False,
                             localization: str = None,
                             db: AsyncSession = Depends(get_db)
                             ) -> Union[list[ShowItem], str]:
    async with db as session:
        async with session.begin():
            item_dal = ItemDAL(session)
            return await item_dal.get_item_from_tag(tag=tag,
                                                    is_tags=is_tags,
                                                    is_subtypes=is_subtypes,
                                                    is_parts=is_parts,
                                                    localization=localization)


# Получение списка предметов с параметром в виде _ВТОРИЧНОГО_ тега
@local_router.get('/items/subtype', response_model=Union[list[ShowItem], str], response_model_exclude_defaults=True)
async def get_items_from_subtype(subtype: str,
                                 is_tags: bool = False,
                                 is_subtypes: bool = False,
                                 is_parts: bool = False,
                                 localization: str = None,
                                 db: AsyncSession = Depends(get_db)
                                 ) -> Union[list[ShowItem], str]:
    async with db as session:
        async with session.begin():
            item_dal = ItemDAL(session)
            return await item_dal.get_item_from_subtype(subtype=subtype,
                                                        is_tags=is_tags,
                                                        is_subtypes=is_subtypes,
                                                        is_parts=is_parts,
                                                        localization=localization)
