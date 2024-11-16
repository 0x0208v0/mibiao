from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from mibiao.models.base import BaseModel


class Setting(BaseModel):
    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    user: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        default='root',
    )

    site_title: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        index=True,
    )
