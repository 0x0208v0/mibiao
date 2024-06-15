import uuid

from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from mibiao.models.base import BaseModel
from mibiao.models.base import UUID


class Domain(BaseModel):
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=False,
    )

    domain: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default='',
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default='',
    )

    rank: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default='0',
    )

    is_hide: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default='0',
    )
