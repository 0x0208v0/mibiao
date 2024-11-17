from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from mibiao.models.base import BaseModel
from mibiao.models.user import UserMixin


class Domain(BaseModel, UserMixin):
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

    def to_dict(self) -> dict:
        return {
            'domain': self.domain,
            'description': self.description,
            'rank': self.rank,
            'is_hide': self.is_hide,
            'display_created_at': self.format_created_at(tz='Asia/Shanghai'),
            'display_updated_at': self.format_updated_at(tz='Asia/Shanghai'),
        }
