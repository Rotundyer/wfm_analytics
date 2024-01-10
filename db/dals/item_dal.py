from uuid import UUID
from typing import Union

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from db.models import Item
from db.models import Tag
from db.models import Subtype
from db.models import PartOfSet
from db.models import Language

from api.models import Item as ShowItem
from api.models import PartOfSet as ShowPartOfSet
from api.models import Language as ShowLanguage


# Класс для работы с таблицой с предметами в БД
class ItemDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # Создание предмета в таблице
    async def create_item(self,
                          wfm_id: str,
                          url_name: str,
                          tradable: bool,
                          trading_tax: int = None,
                          quantity_for_set: int = None,
                          set_root: bool = None,
                          icon: str = None,
                          icon_format: str = None,
                          thumb: str = None,
                          rarity: str = None,
                          max_rank: int = None,
                          mastery_level: int = None,
                          ducats: int = None) -> Union[Item, None]:
        new_item = Item(
            wfm_id=wfm_id,
            url_name=url_name,
            tradable=tradable,
            trading_tax=trading_tax,
            quantity_for_set=quantity_for_set,
            set_root=set_root,
            icon=icon,
            icon_format=icon_format,
            thumb=thumb,
            rarity=rarity,
            max_rank=max_rank,
            mastery_level=mastery_level,
            ducats=ducats
        )
        # Проверка на наличие дубликата в таблице
        query = select(Item).where(Item.wfm_id == wfm_id, Item.url_name == url_name)
        res = await self.db_session.execute(query)
        row = res.fetchone()
        if row is None:
            # Если добавляемое значение уникально, то оно записывается в таблицу
            self.db_session.add(new_item)
            await self.db_session.flush()
            return new_item
        else:
            print(f'{url_name} is already in the Item table')
            return None

    # Получение инфомрации о предмете в зависимости от запрашиваемых параметров
    # is_tags добавляет _ОСНОВНЫЕ_ теги к возвращаемой информации
    # is_subtypes добавляет _ПОБОЧНЫЕ_ теги к возвращаемой информации
    # is_parts добавляет взаимосвязи с другими предметами
    # localization добавялет конкретную локализации или все сразу
    async def get_item(self, item_id: UUID = None,
                       url_name: str = None,
                       wfm_id: str = None,
                       is_tags: bool = False,
                       is_subtypes: bool = False,
                       is_parts: bool = False,
                       localization: str = None) -> Union[ShowItem, str]:
        # Проверка на основные параметры. Поиск происходит по ним
        # Если ни один параметр не ликвиден, то возвращается предупреждение о некорректных данных
        if item_id is not None:
            query = select(Item).where(Item.item_id == item_id)
        else:
            if url_name is not None:
                query = select(Item).where(Item.url_name == url_name)
            else:
                if wfm_id is not None:
                    query = select(Item).where(Item.wfm_id == wfm_id)
                else:
                    return "Search parameters not set"
        # Проверка на дубликат
        res = await self.db_session.execute(query)
        row = res.fetchone()
        if row is not None:
            # Создание модели данных и её пополнение в зависимости от тегов
            item = row[0]
            show_item = ShowItem(
                item_id=item.item_id,
                wfm_id=item.wfm_id,
                url_name=item.url_name,
                tradable=item.tradable,
                trading_tax=item.trading_tax,
                quantity_for_set=item.quantity_for_set,
                set_root=item.set_root,
                icon=item.icon,
                icon_format=item.icon_format,
                thumb=item.thumb,
                rarity=item.rarity,
                max_rank=item.max_rank,
                mastery_level=item.mastery_level,
                ducast=item.ducats
            )
            if is_tags:
                query = select(Tag).where(Tag.item_id == item.item_id)
                res = await self.db_session.execute(query)
                rows = res.fetchall()
                if rows is not None:
                    tags: list[str] = []
                    for row in rows:
                        tags.append(row[0].tag)
                    if len(tags) > 0:
                        show_item.tags = tags
            if is_subtypes:
                query = select(Subtype).where(Subtype.item_id == item.item_id)
                res = await self.db_session.execute(query)
                rows = res.fetchall()
                if rows is not None:
                    subtypes: list[str] = []
                    for row in rows:
                        subtypes.append(row[0].subtype)
                    if len(subtypes) > 0:
                        show_item.subtypes = subtypes
            if is_parts:
                query = select(PartOfSet).where(PartOfSet.item_id == item.item_id)
                res = await self.db_session.execute(query)
                rows = res.fetchall()
                if rows is not None:
                    part_of_set: list[ShowPartOfSet] = []
                    for row in rows:
                        part_of_set.append(ShowPartOfSet(part_id=row[0].part_id, part_name=row[0].part_name))
                    if len(part_of_set) > 0:
                        show_item.part_of_set = part_of_set
            if localization is not None:
                if localization != 'all':
                    query = select(Language).where((Language.item_id == item.item_id) &
                                                   (Language.language == localization))
                else:
                    query = select(Language).where(Language.item_id == item.item_id)
                res = await self.db_session.execute(query)
                rows = res.fetchall()
                if rows is not None:
                    local: dict[str, ShowLanguage] = {}
                    for row in rows:
                        local.update({row[0].language: ShowLanguage(item_name=row[0].item_name,
                                                                    description=row[0].description,
                                                                    wiki_link=row[0].wiki_link)})
                    if len(local) > 0:
                        show_item.localization = local
            return show_item
        else:
            return "There's no such item in the database"

    # Получение информации по нескольком предметам
    # Параметры наполнения такие же, как и у одиночного запроса
    async def get_items(self, items_id: list[UUID] = None,
                        urls_name: list[str] = None,
                        wfms_id: list[str] = None,
                        is_tags: bool = False,
                        is_subtypes: bool = False,
                        is_parts: bool = False,
                        localization: str = None
                        ) -> Union[list[ShowItem], str]:
        items: list[ShowItem] = []
        if items_id is not None:
            for item_id in items_id:
                item = await self.get_item(
                    item_id=item_id,
                    is_tags=is_tags,
                    is_subtypes=is_subtypes,
                    is_parts=is_parts,
                    localization=localization
                )
                if item is not str:
                    items.append(item)
        if urls_name is not None:
            for url_name in urls_name:
                item = await self.get_item(
                    url_name=url_name,
                    is_tags=is_tags,
                    is_subtypes=is_subtypes,
                    is_parts=is_parts,
                    localization=localization
                )
                if item is not str:
                    items.append(item)
        if wfms_id is not None:
            for wfm_id in wfms_id:
                item = await self.get_item(
                    wfm_id=wfm_id,
                    is_tags=is_tags,
                    is_subtypes=is_subtypes,
                    is_parts=is_parts,
                    localization=localization
                )
                if item is not str:
                    items.append(item)
        if items_id is None and urls_name is None and wfms_id is None:
            return "Search parameters not set"
        return items

    # Получение всех предметов, соответствующих _ОСНОВНОМУ_ тегу
    async def get_item_from_tag(self, tag: str,
                                is_tags: bool = False,
                                is_subtypes: bool = False,
                                is_parts: bool = False,
                                localization: str = None) -> Union[list[ShowItem], str]:
        items: list[ShowItem] = []
        item_id_list: list[UUID] = []
        query = select(Tag).where(Tag.tag == tag)
        res = await self.db_session.execute(query)
        rows = res.fetchall()
        if rows is not None:
            for row in rows:
                item_id_list.append(row[0].item_id)
            for item_id in item_id_list:
                item = await self.get_item(item_id=item_id,
                                           is_tags=is_tags,
                                           is_subtypes=is_subtypes,
                                           is_parts=is_parts,
                                           localization=localization)
                if type(item) is not str:
                    items.append(item)
            if len(items) > 0:
                print(items)
                return items
            else:
                return 'No items were found for your request'
        else:
            return f"There were no items found in the database by the tag {tag}"

    # Получение всех предметов, соответствующих _ПОБОЧНОМУ_ тегу
    async def get_item_from_subtype(self, subtype: str,
                                    is_tags: bool = False,
                                    is_subtypes: bool = False,
                                    is_parts: bool = False,
                                    localization: str = None) -> Union[list[ShowItem], str]:
        items: list[ShowItem] = []
        item_id_list: list[UUID] = []
        query = select(Subtype).where(Subtype.subtype == subtype)
        res = await self.db_session.execute(query)
        rows = res.fetchall()
        if rows is not None:
            for row in rows:
                item_id_list.append(row[0].item_id)
            for item_id in item_id_list:
                item = await self.get_item(item_id=item_id,
                                           is_tags=is_tags,
                                           is_subtypes=is_subtypes,
                                           is_parts=is_parts,
                                           localization=localization)
                if type(item) is not str:
                    items.append(item)
            if len(items) > 0:
                print(items)
                return items
            else:
                return 'No items were found for your request'
        else:
            return f"There were no items found in the database by the tag {subtype}"
