from __future__ import annotations

import logging
import os
import pathlib
import secrets

from filelock import FileLock
from flask import Flask
from flask_compress import Compress
from flask_login import LoginManager
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from mibiao.blueprints import register_blueprints
from mibiao.models import db
from mibiao.models import register_models
from mibiao.models.config import load_config
from mibiao.models.tag import Tag
from mibiao.models.user import User
from mibiao.settings import settings
from mibiao.utils.markdown import markdown_to_html as _markdown_to_html

logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

app = Flask(__name__, instance_path=os.getcwd())
app.config.update(settings.to_dict())

app.json.ensure_ascii = False
app.json.mimetype = 'application/json; charset=utf-8'

Compress(app)

login_manager = LoginManager(app)
login_manager.login_view = 'user.login'
login_manager.login_message = '访问该页面需要先登陆'


@login_manager.user_loader
def load_user(user_id: str):
    return User.get(user_id)


@app.errorhandler(IntegrityError)
@app.errorhandler(ValueError)
@app.errorhandler(HTTPException)
def handle_validation_error(error):
    return {'err': {'msg': str(error)}}, 400


register_models(app)
register_blueprints(app)


@app.context_processor
def context_processor():
    config = load_config()
    tag_list = Tag.get_list(
        Tag.is_hide == False,
        order_by=[
            Tag.rank,
            Tag.id.desc(),
        ],
    )
    return {
        'config': config,
        'tag_list': tag_list,
    }


@app.template_filter('markdown_to_html')
def markdown_to_html(s):
    return _markdown_to_html(s)


with app.app_context():
    db.create_all()

    env_file_path = pathlib.Path('.env')
    if not env_file_path.exists():
        with FileLock('.env.lock') as lock:
            if not env_file_path.exists():
                with open('.env', 'w+') as f:
                    secret_key = secrets.token_hex(16)
                    f.write(f'SECRET_KEY={secret_key}')
