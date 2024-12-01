from flask import Blueprint
from flask import request
from flask_login import login_required

from mibiao.models.config import load_config

blueprint = Blueprint('config', __name__)


@blueprint.get('/api/configs')
@login_required
def get_config_list():
    config = load_config()
    return {'config': config.to_dict()}


@blueprint.post('/api/configs')
@login_required
def save_config_list():
    config = load_config()
    config.save(request.json['config'])
    return {'config': config.to_dict()}
