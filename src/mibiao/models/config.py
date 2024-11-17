from enum import StrEnum

from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from mibiao.models.base import BaseModel


class ConfigItemType(StrEnum):
    INT = 'int'
    TEXT = 'text'


class Config(BaseModel):
    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        index=True,
    )

    type: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        index=True,
    )

    int_value: Mapped[int] = mapped_column(
        Integer
    )

    float_value: Mapped[float] = mapped_column(
        Float
    )

    text_value: Mapped[str] = mapped_column(
        Text
    )
