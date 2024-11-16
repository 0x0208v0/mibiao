import datetime
from datetime import datetime
from typing import Self

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Select
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class SqlalchemyBaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        server_default=func.current_timestamp(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        server_default=func.current_timestamp(),
        onupdate=lambda: datetime.utcnow(),
        server_onupdate=func.current_timestamp(),
    )

    def save(self, commit: bool = True):
        db.session.add(self)
        db.session.flush([self])
        if commit:
            db.session.commit()

    def delete(self, commit: bool = True):
        db.session.delete(self)
        db.session.flush()
        if commit:
            db.session.commit()

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
    def get_one(cls, *where) -> Self | None:
        stmt = select(cls).where(*where)
        result = db.session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    def build_stmt(
        cls,
        *where,
        order_by: list | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> Select:
        stmt = select(cls)

        if where:
            stmt = stmt.where(*where)
        if order_by:
            stmt = stmt.order_by(*order_by)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        return stmt

    @classmethod
    def count(cls, *where) -> int:
        subquery = cls.build_stmt(*where).subquery()
        stmt = select(func.count(subquery.c.id).label('cnt'))
        result = db.session.execute(stmt)
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
        stmt = cls.build_stmt(*where, order_by=order_by, offset=offset, limit=limit)
        result = db.session.execute(stmt).scalars()
        return list(result)

    @classmethod
    def get_list_by_page(
        cls,
        *where,
        order_by: list | None = None,
        page_num: int = 1,
        page_size: int = 20,
    ) -> list[Self]:
        if not order_by:
            order_by = [cls.created_at.desc(), cls.id.desc()]
        return cls.get_list(
            *where,
            order_by=order_by,
            offset=(page_num - 1) * page_size,
            limit=page_size,
        )

    @classmethod
    def get_id_name_list(cls, *where, order_by: list | None = None) -> list:
        subquery = cls.build_stmt(*where, order_by=order_by).subquery()
        stmt = select(subquery.c.id, subquery.c.name)
        result = db.session.execute(stmt)
        id_list = [(id, name) for (id, name) in result]
        return id_list


db = SQLAlchemy(
    model_class=SqlalchemyBaseModel,
    engine_options={'pool_size': 2, 'pool_recycle': 10, 'pool_pre_ping': True},
    session_options={
        'autocommit': False,
        'autoflush': False,
        'expire_on_commit': False,
    },
)

BaseModel: type[SqlalchemyBaseModel] = db.Model
