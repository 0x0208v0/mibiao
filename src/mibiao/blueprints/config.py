from flask import Blueprint
from flask import request
from flask_login import current_user
from flask_login import login_required

from mibiao.models.config import load_config_by_user

blueprint = Blueprint('config', __name__)


@blueprint.get('/api/configs')
@login_required
def get_config_list():
    config = load_config_by_user(current_user)
    return {'config': config.to_dict()}


@blueprint.post('/api/configs')
@login_required
def save_config_list():
    config = load_config_by_user(current_user)
    config.save(request.json['config'])
    return {'config': config.to_dict()}
