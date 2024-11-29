from typing import Self

from flask_login import UserMixin as LoginUserMixin
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import foreign
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from mibiao.models.base import BaseModel
from mibiao.utils.password import check_password_hash
from mibiao.utils.password import generate_password_hash


class User(BaseModel, LoginUserMixin):
    email: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        comment='邮箱',
    )

    password_hash: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        comment='密码HASH',
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default='1',
        comment='是否活跃',
    )

    name: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        comment='名称',
    )

    avatar_url: Mapped[str] = mapped_column(
        String(256),
        unique=True,
        index=True,
        nullable=False,
        comment='头像URL',
    )

    comment: Mapped[str] = mapped_column(
        Text,
        unique=True,
        index=True,
        nullable=False,
        comment='头像URL',
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'display_created_at': self.format_created_at(tz='Asia/Shanghai'),
            'avatar_url': self.avatar_url,
            'comment': self.comment,
        }

    @property
    def username(self) -> str:
        return self.email.split('@')[0]

    @property
    def password(self):
        raise ValueError('can not read password')

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_by_email(cls, email: str) -> Self | None:
        email = email.strip()
        if not email:
            return
        return cls.get_one(cls.email == email)

    @classmethod
    def login(cls, email: str, password: str) -> Self:
        email = (email or '').strip()
        cls.validate_email(email)

        password = (password or '').strip()
        cls.validate_password(password)

        user = cls.get_by_email(email)
        if user is None or not user.is_active or not user.verify_password(password):
            raise ValueError('用户不存在或密码不对')

        return user

    @classmethod
    def validate_email(cls, email: str):
        if not email:
            raise ValueError('邮箱不能为空')

    @classmethod
    def validate_password(cls, password: str):
        if not password:
            raise ValueError('密码不能为空')

    @classmethod
    def register(cls, email: str, password: str, commit: bool = True) -> Self:
        email = (email or '').strip()
        cls.validate_email(email)

        password = (password or '').strip()
        cls.validate_password(password)

        user = cls.get_by_email(email)
        if user:
            raise ValueError('用户已存在')

        user = cls(email=email)
        user.password = password
        user.save(commit=commit)
        return user


class UserMixin:
    user_id: Mapped[str] = mapped_column(
        String(22),
        nullable=False,
    )

    @declared_attr
    @classmethod
    def user(cls) -> Mapped[User]:
        return relationship(
            User,
            primaryjoin=User.id == foreign(cls.user_id),
            lazy='selectin',
            uselist=False,
        )

    def verify_owner(self, user: User):
        if self.user_id != user.id:
            raise ValueError(f'没有权限操作资源 `{self}`')


def get_user_id(user_or_id: User | int) -> int:
    return user_or_id if isinstance(user_or_id, int) else user_or_id.id
