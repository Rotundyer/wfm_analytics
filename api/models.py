import uuid

from typing import Union
from pydantic import BaseModel


# Параметры моделей API
class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict to json"""

        orm_mode = True


# Модель связи между предметами
class PartOfSet(TunedModel):
    part_id: uuid.UUID
    part_name: str


# Модель локализации
class Language(TunedModel):
    item_name: str
    description: Union[str, None] = None
    wiki_link: Union[str, None] = None


# Модель предмета
class Item(TunedModel):
    item_id: uuid.UUID
    wfm_id: str
    url_name: str
    tradable: bool
    trading_tax: Union[int, None] = None
    quantity_for_set: Union[int, None] = None
    set_root: Union[bool, None] = None
    icon: Union[str, None] = None
    icon_format: Union[str, None] = None
    thumb: Union[str, None] = None
    rarity: Union[str, None] = None
    max_rank: Union[int, None] = None
    mastery_level: Union[int, None] = None
    ducats: Union[int, None] = None

    tags: Union[list[str], None] = None
    subtypes: Union[list[str], None] = None
    part_of_set: Union[list[PartOfSet], None] = None
    localization: Union[dict[str, Language], None] = None


# Модель _ОСНОВНОГО_ тэга предмета
class Tag(TunedModel):
    id: int
    tag: str


# Модель _ПОБОЧНОГО_ тэга предмета
class Subtype(TunedModel):
    id: int
    subtype: str


# Модель получения информации о запросе списка с предметами
class GetItems(BaseModel):
    items_id: Union[list[uuid.UUID], None] = None
    wfms_id: Union[list[str], None] = None
    urls_name: Union[list[str], None] = None