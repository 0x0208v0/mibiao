from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Self
from typing import TYPE_CHECKING

import pendulum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Select
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import object_session
from werkzeug.exceptions import NotFound

if TYPE_CHECKING:
    from mibiao.models.user import User


class JsonEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field, uuid.UUID):
            return str(field)
        else:
            return super().default(field)


class SqlalchemyBaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: pendulum.now('UTC'),
        server_default=func.current_timestamp(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: pendulum.now('UTC'),
        server_default=func.current_timestamp(),
        onupdate=lambda: pendulum.now('UTC'),
        server_onupdate=func.current_timestamp(),
    )

    def format_created_at(self, fmt='%Y-%m-%d %H:%M:%S', tz='UTC') -> str:
        return pendulum.from_timestamp(self.created_at.timestamp(), tz).strftime(fmt)

    def format_updated_at(self, fmt='%Y-%m-%d %H:%M:%S', tz='UTC') -> str:
        return pendulum.from_timestamp(self.updated_at.timestamp(), tz).strftime(fmt)

    @property
    def session(self) -> Session:
        return object_session(self)

    @classmethod
    def create(cls, data: dict, *, user: User | None = None, commit: bool = True) -> Self:
        obj = cls(**data)
        if user:
            obj.user_id = user.id
        db.session.add(obj)
        db.session.flush()
        if commit:
            db.session.commit()
        return obj

    def update(self, data: dict, commit: bool = True):
        for k, v in data.items():
            if hasattr(self, k) and k not in {'id', 'created_at', 'updated_at', 'user_id'}:
                setattr(self, k, v)
        db.session.add(self)
        db.session.flush([self])
        if commit:
            db.session.commit()

    def delete(self, commit: bool = True):
        db.session.delete(self)
        db.session.flush([self])
        if commit:
            db.session.commit()

    def save(self, commit: bool = True):
        db.session.add(self)
        db.session.flush([self])
        if commit:
            db.session.commit()

    def to_dict(self) -> dict:
        return {column.name: getattr(self, column.name, None) for column in getattr(self, '__table__').columns}

    def to_json(self, decoder_cls=None) -> str:
        return json.dumps(self.to_dict(), cls=decoder_cls or JsonEncoder)

    @classmethod
    def get_obj_id(cls, obj_or_id: Self | int) -> int:
        if isinstance(obj_or_id, int):
            return obj_or_id
        elif isinstance(obj_or_id, cls):
            return obj_or_id.id
        else:
            obj_id = getattr(obj_or_id, 'id', None)
            if obj_id is None:
                raise ValueError(f'obj {obj_or_id} 没有ID')
            return obj_id

    @classmethod
    def get(cls, ident) -> Self | None:
        return db.session.get(cls, ident)

    @classmethod
    def get_or_404(cls, ident) -> Self:
        obj = cls.get(ident)
        if obj is None:
            raise NotFound(f'{cls.__name__} {ident} 不存在')
        return obj

    @classmethod
    def get_one(cls, *where, user: User | None = None) -> Self | None:
        extra_filters = []
        if user:
            extra_filters.append(cls.user_id == user.id)
        query = select(cls).where(*where, *extra_filters)
        result = db.session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    def get_one_or_404(cls, *where, user: User | None = None) -> Self:
        obj = cls.get_one(*where, user=user)
        if obj is None:
            raise NotFound(f'{cls.__name__} 不存在')
        return obj

    @classmethod
    def build_query(
            cls,
            *where,
            order_by: list | None = None,
            offset: int | None = None,
            limit: int | None = None,
            user: User | None = None,
    ) -> Select:
        query = select(cls)
        extra_filters = []
        if user:
            extra_filters.append(cls.user_id == user.id)
        if where:
            query = query.where(*where, *extra_filters)
        if order_by:
            query = query.order_by(*order_by)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query

    @classmethod
    def count(cls, *where, user: User | None = None) -> int:
        subquery = cls.build_query(*where, user=user).subquery()
        query = select(func.count(subquery.c.id).label('count'))
        result = db.session.execute(query)
        for (cnt,) in result:
            return cnt

    @classmethod
    def get_list(
            cls,
            *where,
            order_by: list | None = None,
            offset: int | None = None,
            limit: int | None = None,
            user: User | None = None,
    ) -> list[Self]:
        query = cls.build_query(
            *where,
            order_by=order_by,
            offset=offset,
            limit=limit,
            user=user,
        )
        result = db.session.execute(query).scalars()
        return list(result)

    @classmethod
    def get_list_by_page(
            cls,
            *where,
            order_by: list | None = None,
            page_num: int = 1,
            page_size: int = 20,
            user: User | None = None,
    ) -> list[Self]:
        if not order_by:
            order_by = [cls.id]
        return cls.get_list(
            *where,
            order_by=order_by,
            offset=(page_num - 1) * page_size,
            limit=page_size,
            user=user,
        )


db = SQLAlchemy(
    model_class=SqlalchemyBaseModel,
    engine_options={
        'pool_size': 2,
        'pool_recycle': 10,
        'pool_pre_ping': True,

        # SQLAlchemy Memory Leak: https://github.com/sqlalchemy/sqlalchemy/discussions/6573
        # Potential memory leak? https://github.com/sqlalchemy/sqlalchemy/discussions/9726
        'query_cache_size': 0,
    },
    session_options={
        'autocommit': False,
        'autoflush': False,
        'expire_on_commit': False,
    },
)

BaseModel: type[SqlalchemyBaseModel] = db.Model

session = db.session
