from typing import Self

from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import delete
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from mibiao.models.base import BaseModel
from mibiao.models.tag import DomainTag
from mibiao.models.tag import Tag
from mibiao.models.user import User
from mibiao.models.user import UserMixin


class Domain(BaseModel, UserMixin):
    name: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        index=True,
        comment='名称',
    )

    icon_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default='',
        comment='域名图标URL',
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default='',
        comment='域名描述',
    )

    selling_price: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default='',
        comment='售价',
    )

    renewal_price: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default='',
        comment='续费价格',
    )

    transaction_method: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default='',
        comment='交易方式',
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

    tags: Mapped[list[Tag]] = relationship(
        Tag,
        secondary=DomainTag.__table__,
        primaryjoin='Domain.id == DomainTag.domain_id',
        secondaryjoin='DomainTag.tag_id == Tag.id',
    )

    @classmethod
    def create(
            cls, data: dict, *, user: User | None = None, commit: bool = True,
    ) -> Self:
        data['tags'] = Tag.get_list_by_ids(data.pop('tag_ids'))
        return super().create(data=data, user=user, commit=commit)

    def update(self, data: dict, commit: bool = True):
        data['tags'] = Tag.get_list_by_ids(data.pop('tag_ids'))
        return super().update(data=data, commit=commit)

    def update_tags(self, tag_ids: list[str], commit: bool = True):
        tags = Tag.get_list_by_ids(tag_ids)
        self.tags = tags
        self.session.flush([self])
        if commit:
            self.session.commit()

    def remove_tags(self, tag_ids: list[str], commit: bool = True):
        self.session.execute(
            delete(DomainTag)
            .where(
                DomainTag.domain_id == self.id,
                DomainTag.tag_id.in_(tag_ids),
            )
        )
        self.session.flush([self])
        if commit:
            self.session.commit()

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'icon_url': self.icon_url,
            'description': self.description,
            'selling_price': self.selling_price,
            'renewal_price': self.renewal_price,
            'transaction_method': self.transaction_method,
            'rank': self.rank,
            'is_hide': self.is_hide,
            'display_created_at': self.format_created_at(tz='Asia/Shanghai'),
            'display_updated_at': self.format_updated_at(tz='Asia/Shanghai'),
            'tag_ids': [tag.id for tag in self.tags],
            'tags': [tag.to_dict() for tag in self.tags],
        }
