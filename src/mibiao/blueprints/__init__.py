from __future__ import annotations

from flask import Flask

from mibiao.blueprints import admin
from mibiao.blueprints import config
from mibiao.blueprints import domain
from mibiao.blueprints import main
from mibiao.blueprints import tag
from mibiao.blueprints import user


def register_blueprints(app: Flask):
    app.register_blueprint(admin.blueprint)
    app.register_blueprint(config.blueprint)
    app.register_blueprint(domain.blueprint)
    app.register_blueprint(main.blueprint)
    app.register_blueprint(tag.blueprint)
    app.register_blueprint(user.blueprint)
