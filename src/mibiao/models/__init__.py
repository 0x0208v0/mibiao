from sqlalchemy_utils import force_instant_defaults

force_instant_defaults()

from flask import Flask

from mibiao.models.base import db
from mibiao.models.config import Config
from mibiao.models.domain import Domain
from mibiao.models.tag import Tag
from mibiao.models.user import User

__all__ = [
    'db', 'Config', 'Domain', 'Tag', 'User', 'register_models',
]


def register_models(app: Flask):
    db.init_app(app)
