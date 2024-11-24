from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from mibiao.models.base import BaseModel
from mibiao.models.user import UserMixin


class Tag(BaseModel, UserMixin):
    name: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        index=True,
        comment='名称',
    )

    url_path_name: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        index=True,
        comment='URL路径名',
    )

    rank: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default='0',
        comment='顺序',
    )

    is_hide: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default='0',
        comment='是否隐藏',
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'url_path_name': self.url_path_name,
            'rank': self.rank,
            'is_hide': self.is_hide,
            'display_created_at': self.format_created_at(tz='Asia/Shanghai'),
            'display_updated_at': self.format_updated_at(tz='Asia/Shanghai'),
        }

    def delete(self, commit: bool = True):
        if DomainTag.count(DomainTag.tag_id == self.id):
            raise ValueError('标签已被使用，无法删除')
        super().delete(commit)


class DomainTag(BaseModel):
    tag_id: Mapped[str] = mapped_column(
        String(22),
        nullable=False,
    )

    domain_id: Mapped[str] = mapped_column(
        String(22),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(tag_id, domain_id),
    )
