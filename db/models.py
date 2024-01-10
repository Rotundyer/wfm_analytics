import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

# Модели, на основе которых создаются таблицы в БД и работает SQLalchemy

Base = declarative_base()


# Модель предмета
class Item(Base):
    __tablename__ = "items"

    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wfm_id = Column(String, nullable=False, unique=True)
    url_name = Column(String, nullable=False, unique=True)
    tradable = Column(Boolean, nullable=False)

    trading_tax = Column(Integer, nullable=True)
    quantity_for_set = Column(Integer, nullable=True)
    set_root = Column(Boolean, nullable=True)
    icon = Column(String, nullable=True)
    icon_format = Column(String, nullable=True)
    thumb = Column(String, nullable=True)

    rarity = Column(String, nullable=True)
    max_rank = Column(Integer, nullable=True)

    mastery_level = Column(Integer, nullable=True)
    ducats = Column(Integer, nullable=True)


# Модель заказа
class Orders(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)
    platinum = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=True)
    order_type = Column(String, nullable=True)
    platform = Column(String, default='pc')
    region = Column(String, nullable=True)
    creation_date = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, nullable=True)
    visible = Column(Boolean, nullable=False)
    user_id = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    reputation = Column(Integer, nullable=True)


# Модель связей между предметами
class PartOfSet(Base):
    __tablename__ = 'part_of_set'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(UUID(as_uuid=True), nullable=False)
    part_id = Column(UUID(as_uuid=True), nullable=False)
    main_name = Column(String, nullable=False)
    part_name = Column(String, nullable=False)


# Модель связей _ОСНОВНЫХ_ тегов и предметов
class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(UUID(as_uuid=True), nullable=False)
    tag = Column(String, nullable=False)


# Модель уникальных _ОСНОВНЫХ_ тегов
class ValueTag(Base):
    __tablename__ = 'value_tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String, nullable=False, unique=True)


# Модель связей _ПОБОЧНЫХ тегов и предметов
class Subtype(Base):
    __tablename__ = 'subtypes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(UUID(as_uuid=True), nullable=False)
    subtype = Column(String, nullable=False)


# Модель уникальных _ПОБОЧНЫХ тегов
class ValueSubtype(Base):
    __tablename__ = 'value_subtypes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    subtype = Column(String, nullable=False, unique=True)


# Модель локализаций
class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(UUID(as_uuid=True), nullable=False)
    language = Column(String, nullable=False)
    item_name = Column(String, nullable=False)
    description = Column(String)
    wiki_link = Column(String)
