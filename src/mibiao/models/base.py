from __future__ import annotations

import json
import uuid
from datetime import datetime
from json import JSONEncoder
from typing import Self

import pendulum
import shortuuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy import Select
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import object_session
from werkzeug.exceptions import NotFound


class JsonEncoder(JSONEncoder):
    def default(self, field):
        if isinstance(field, uuid.UUID):
            return str(field)
        elif isinstance(field, datetime):
            return field.isoformat()
        else:
            return super().default(field)


class SqlalchemyBaseModel(DeclarativeBase):
    id: Mapped[str] = mapped_column(
        String(22),
        primary_key=True,
        default=shortuuid.uuid,
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
    def create_from_data(
            cls,
            data: dict,
            *,
            commit: bool = True,
    ) -> Self:
        obj = cls(**data)
        db.session.add(obj)
        db.session.flush([obj])
        if commit:
            db.session.commit()
        return obj

    @classmethod
    def create(
            cls,
            data: dict,
            *,
            commit: bool = True,
    ):
        return cls.create_from_data(data=data, commit=commit)

    def update_from_data(self, data: dict, commit: bool = True):
        for k, v in data.items():
            if hasattr(self, k) and k not in {
                'id',
                'created_at',
                'updated_at',
            }:
                setattr(self, k, v)
        db.session.add(self)
        db.session.flush([self])
        if commit:
            db.session.commit()

    def update(self, data: dict, commit: bool = True):
        return self.create_from_data(data=data, commit=commit)

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

    def to_record(self) -> dict:
        return {column.name: getattr(self, column.name, None) for column in getattr(self, '__table__').columns}

    def to_json(self, decoder_cls: JSONEncoder | None = None) -> str:
        return json.dumps(self.to_record(), cls=decoder_cls or JsonEncoder)

    def to_dict(self) -> dict:
        return {column.name: getattr(self, column.name, None) for column in getattr(self, '__table__').columns}

    @classmethod
    def export_to_json_str(
            cls,
            ensure_ascii: bool = False,
            indent: int = 4,
            decoder_cls: JSONEncoder | None = None,
    ) -> str:
        obj_list = []
        for obj in cls.get_list():
            obj_list.append(json.loads(obj.to_json()))
        return json.dumps(obj_list, ensure_ascii=ensure_ascii, indent=indent, cls=decoder_cls or JsonEncoder)

    @classmethod
    def import_from_json_str(cls, json_str: str):
        json_data = json.loads(json_str)
        for obj in cls.get_list():
            obj.delete()

        if isinstance(json_data, list):
            data_list = json_data
        else:
            data_list = [json_data]

        for data in data_list:
            if 'updated_at' in data:
                data['updated_at'] = datetime.fromisoformat(data['updated_at'])
            if 'created_at' in data:
                data['created_at'] = datetime.fromisoformat(data['created_at'])
            cls.create_from_data(data)

    @classmethod
    def get_obj_id(cls, obj_or_id: Self | str) -> str:
        if isinstance(obj_or_id, str):
            return obj_or_id
        elif isinstance(obj_or_id, cls):
            return obj_or_id.id
        else:
            obj_id = getattr(obj_or_id, 'id', None)
            if obj_id is None:
                raise ValueError(f'obj {obj_or_id} 没有ID')
            return obj_id

    @classmethod
    def get(cls, ident: str) -> Self | None:
        return db.session.get(cls, ident)

    @classmethod
    def get_or_404(cls, ident) -> Self:
        obj = cls.get(ident)
        if obj is None:
            raise NotFound(f'{cls.__name__} {ident} 不存在')
        return obj

    @classmethod
    def get_one(cls, *where) -> Self | None:
        query = select(cls).where(*where)
        result = db.session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    def get_one_or_404(cls, *where) -> Self:
        obj = cls.get_one(*where)
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
    ) -> Select:
        query = select(cls)
        if where:
            query = query.where(*where)
        if order_by:
            query = query.order_by(*order_by)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query

    @classmethod
    def count(cls, *where) -> int:
        subquery = cls.build_query(*where).subquery()
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
    ) -> list[Self]:
        query = cls.build_query(
            *where,
            order_by=order_by,
            offset=offset,
            limit=limit,
        )
        return list(db.session.execute(query).scalars())

    @classmethod
    def get_list_by_ids(cls, ids: list[str]) -> list[Self]:
        if not ids:
            return []
        query = cls.build_query(cls.id.in_(ids))
        return list(db.session.execute(query).scalars())

    @classmethod
    def get_list_by_page(
            cls,
            *where,
            order_by: list | None = None,
            page_num: int = 1,
            page_size: int = 20,
    ) -> list[Self]:
        if not order_by:
            order_by = [cls.id]
        return cls.get_list(
            *where,
            order_by=order_by,
            offset=(page_num - 1) * page_size,
            limit=page_size,
        )


db = SQLAlchemy(
    model_class=SqlalchemyBaseModel,
    engine_options={
        'pool_size': 1,
        'pool_recycle': 100,
        'pool_pre_ping': True,
    },
    session_options={
        'autocommit': False,
        'autoflush': False,
        'expire_on_commit': False,
    },
)

BaseModel: type[SqlalchemyBaseModel] = db.Model

session = db.session
