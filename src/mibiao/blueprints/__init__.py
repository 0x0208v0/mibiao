from flask import Flask

from mibiao.blueprints import admin
from mibiao.blueprints import domain
from mibiao.blueprints import main
from mibiao.blueprints import user


def register_blueprints(app: Flask):
    app.register_blueprint(admin.blueprint)
    app.register_blueprint(domain.blueprint)
    app.register_blueprint(main.blueprint)
    app.register_blueprint(user.blueprint)
