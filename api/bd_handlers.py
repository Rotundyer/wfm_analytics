from os import listdir as os_listdir
from json import load as json_load

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals.item_dal import ItemDAL
from db.dals.value_tag_dal import ValueTagDAL
from db.dals.value_subtype_dal import ValueSubtypeDAL
from db.dals.subtype_dal import SubtypeDAL
from db.dals.tag_dal import TagDAL
from db.dals.language_dal import LanguageDAL
from db.dals.part_of_set_dal import PartOfSetDAL

from db.session import get_db

from untils.items_info_update import items_download

db_router = APIRouter()


# Пополнение таблиц локальными данными из папки temple
# Актуальные данные по пути temple/wfm-items-master/items
@db_router.post('/update_tables')
async def value_tags_db(db: AsyncSession = Depends(get_db)):
    # Закачака данных из github в виде zipfile и его разорхивации
    # https://github.com/42bytes-team/wfm-items
    items_download()
    # Создание сессии для работы с БД
    async with db as session:
        async with session.begin():
            # Подключение DAL классов для прямой работы с БД
            value_tags_dal = ValueTagDAL(session)
            value_subtype_dal = ValueSubtypeDAL(session)
            item_dal = ItemDAL(session)
            subtype_dal = SubtypeDAL(session)
            tag_dal = TagDAL(session)
            language_dal = LanguageDAL(session)
            part_of_set_dal = PartOfSetDAL(session)

            directory = './temple/wfm-items-master/tracked/items'
            files = os_listdir(directory)

            tags = []
            subtypes = []

            # Проход по каждому файлу и распарс данных
            for file in files:
                with open(f'{directory}/{file}', 'r', encoding='utf-8') as f:
                    json = json_load(f)

                    # Создание модели предмета и добавление его в БД
                    _item = CreateItem(json)
                    item = await item_dal.create_item(
                        wfm_id=_item.wfm_id,
                        url_name=_item.url_name,
                        tradable=_item.tradable,
                        trading_tax=_item.trading_tax,
                        quantity_for_set=_item.quantity_for_set,
                        set_root=_item.set_root,
                        icon=_item.icon,
                        icon_format=_item.icon_format,
                        thumb=_item.thumb,
                        rarity=_item.rarity,
                        max_rank=_item.max_rank,
                        mastery_level=_item.mastery_level,
                        ducats=_item.ducats
                    )

                    # Проверка на то, добавлен ли предмет в БД
                    # Если предмет дублируется или произошла ошибка при добавлении, то связанные элементы в БД не добавляются
                    if item is not None:
                        #
                        # TODO: Добавить обработку дубликатов локализации и связей тэгов в БД
                        #
                        # Добавление локализаций предмета
                        for language in json['i18n']:
                            try:
                                item_name = json['i18n'][language]['item_name']
                            except:
                                item_name = 'error'
                            try:
                                description = json['i18n'][language]['description']
                            except:
                                description = None
                            try:
                                wiki_link = json['i18n'][language]['wiki_link']
                            except:
                                wiki_link = None
                            await language_dal.create_language(item_id=item.item_id,
                                                               language=language,
                                                               item_name=item_name,
                                                               description=description,
                                                               wiki_link=wiki_link)

                        # Обработка и добавление уникальных _ОСНОВНЫХ_ тегов и тегов, связанных с предметом
                        try:
                            _tags = []
                            for tag in json['tags']:
                                if tag not in tags:
                                    tags.append(tag)
                                    _tags.append(tag)
                                await tag_dal.create_tag(item_id=item.item_id, tag=tag)

                            for tag in _tags:
                                await value_tags_dal.create_value_tag(tag=tag)
                        except:
                            pass

                        # Обработка и добавление уникальных _ПОБОЧНЫХ_ тегов и тегов, связанных с предметом
                        try:
                            _subtypes = []
                            for subtype in json['subtypes']:
                                if subtype not in subtypes:
                                    subtypes.append(subtype)
                                    _subtypes.append(subtype)
                                await subtype_dal.create_subtype(item_id=item.item_id, subtype=subtype)

                            for subtype in _subtypes:
                                await value_subtype_dal.create_value_subtype(subtype=subtype)
                        except:
                            pass

            # Создание взаимосвязей между предметами
            # Пример: части одного сета
            for file in files:
                with open(f'{directory}/{file}', 'r', encoding='utf-8') as f:
                    json = json_load(f)

                    url_name = json['url_name']
                    try:
                        for part in json['part_of_set']:
                            await part_of_set_dal.create_part_of_set_with_str(main_name=url_name, part_name=part)
                    except:
                        continue
        return 'completed'


# Класс для проверки данных на существование и обработку обратного
class CreateItem:
    def __init__(self, json):
        self.wfm_id = json['_id']
        self.url_name = json['url_name']
        try:
            self.tradable = json['tradable']
        except:
            self.tradable = False
        try:
            self.trading_tax = json['trading_tax']
        except:
            self.trading_tax = None
        try:
            self.quantity_for_set = json['quantity_for_set']
        except:
            self.quantity_for_set = None
        try:
            self.set_root = json['set_root']
        except:
            self.set_root = None
        try:
            self.icon = json['icon']
        except:
            self.icon = None
        try:
            self.icon_format = json['icon_format']
        except:
            self.icon_format = None
        try:
            self.thumb = json['thumb']
        except:
            self.thumb = None
        try:
            self.rarity = json['rarity']
        except:
            self.rarity = None
        try:
            self.max_rank = json['max_rank']
        except:
            self.max_rank = None
        try:
            self.mastery_level = json['mastery_level']
        except:
            self.mastery_level = None
        try:
            self.ducats = json['ducats']
        except:
            self.ducats = None
