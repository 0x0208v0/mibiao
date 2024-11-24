from __future__ import annotations

from enum import StrEnum
from typing import Self

from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from mibiao.models.base import BaseModel
from mibiao.models.base import session
from mibiao.models.user import User
from mibiao.models.user import UserMixin
from mibiao.models.user import get_user_id


class ConfigItemValueType(StrEnum):
    INT = 'int'
    FLOAT = 'float'
    TEXT = 'text'
    NONE = 'none'


class ConfigItem(BaseModel, UserMixin):
    name: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        index=True,
    )

    value_type: Mapped[str] = mapped_column(
        String(256),
    )

    int_value: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    float_value: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )

    text_value: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    def get_value(self) -> int | float | str | None:
        if self.value_type == ConfigItemValueType.INT:
            return self.int_value
        elif self.value_type == ConfigItemValueType.FLOAT:
            return self.float_value
        elif self.value_type == ConfigItemValueType.TEXT:
            return self.text_value

    @classmethod
    def guess_value_type(cls, value: int | float | str | None) -> ConfigItemValueType:
        if isinstance(value, int):
            return ConfigItemValueType.INT
        elif isinstance(value, float):
            return ConfigItemValueType.FLOAT
        elif isinstance(value, str):
            return ConfigItemValueType.TEXT
        else:
            return ConfigItemValueType.NONE

    def set_value(self, value: int | float | str | None, value_type: ConfigItemValueType | None = None):
        if value_type is None:
            self.value_type = self.guess_value_type(value)
        else:
            self.value_type = ConfigItemValueType(value_type)
        if self.value_type == ConfigItemValueType.INT:
            self.int_value = value
        elif self.value_type == ConfigItemValueType.FLOAT:
            self.float_value = value
        elif self.value_type == ConfigItemValueType.TEXT:
            self.text_value = value

    @classmethod
    def items_to_dict(cls, items: list[Self]) -> dict:
        return {item.name: item for item in items}

    def to_dict(self):
        return {
            'name': self.name,
            'value': self.get_value(),
        }


class Item:

    def __init__(self, name: str | None = None, default_value=None):
        self.name = name
        self.default_value = default_value

    def __set_name__(self, owner: type[Config], name):
        _item_name_set = getattr(owner, '__item_name_set__', None)
        if _item_name_set is None:
            _item_name_set = set()
            setattr(owner, '__item_name_set__', _item_name_set)
        _item_name_set.add(name)
        if self.name is None:
            self.name = name

    def __get__(self, instance: Config, owner):
        if self.name in instance.item_dict:
            return instance.item_dict[self.name].get_value()
        else:
            return self.default_value

    def __set__(self, instance: Config, value):
        if self.name not in instance.item_dict:
            instance.item_dict[self.name] = ConfigItem(user_id=instance.user_id, name=self.name)
        instance.item_dict[self.name].set_value(value)


class Config:
    __item_name_set__: set

    site_title: str = Item(default_value='DomainSeek')

    site_icon_url: str = Item(
        default_value='https://www.nodeseek.com/static/image/favicon/android-chrome-192x192.png'
    )

    site_brand: str = Item(default_value='DomainSeek')

    site_beta: str = Item(default_value='beta')

    site_copyright: str = Item(default_value='Copyright © 2024 - 2025 All rights Reserved')

    def __init__(self, user_id: int, items: list[ConfigItem] | None = None):
        self.user_id: int = user_id
        self.item_dict: dict = {item.name: item for item in (items or [])}

    @classmethod
    def validate_item_name(cls, name: str):
        if name not in cls.__item_name_set__:
            raise ValueError(f'`{name}`不是有效的配置项`')

    def save(self, data: dict | None = None):
        for name, value in (data or {}).items():
            self.validate_item_name(name)
            setattr(self, name, value)
        if data:
            session.add_all(list(self.item_dict.values()))
            session.commit()

    def to_dict(self) -> dict:
        return {name: getattr(self, name) for name in self.__item_name_set__}


def load_config_by_user(user_or_id: User | int) -> Config:
    user_id = get_user_id(user_or_id)
    items = ConfigItem.get_list(ConfigItem.user_id == user_id)
    return Config(user_id, items)
