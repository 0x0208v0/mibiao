from sqlalchemy_utils import force_instant_defaults

force_instant_defaults()

from flask import Flask

from mibiao.models.base import db
from mibiao.models.domain import Domain
from mibiao.models.setting import Setting
from mibiao.models.user import User


def register_models(app: Flask):
    db.init_app(app)
