from typing import Self

from flask_login import UserMixin
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from mibiao.models.base import BaseModel
from mibiao.utils.password import check_password_hash
from mibiao.utils.password import generate_password_hash


class User(BaseModel, UserMixin):
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

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'display_created_at': self.format_created_at(tz='Asia/Shanghai'),
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
