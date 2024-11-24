import logging

from flask import Blueprint
from flask import request
from flask_login import current_user
from flask_login import login_required

from mibiao.models.tag import Tag

logger = logging.getLogger(__name__)

blueprint = Blueprint('tag', __name__)


@blueprint.get('/api/tags')
@login_required
def get_tag_list():
    tag_list = Tag.get_list(
        order_by=[Tag.is_hide, Tag.rank, Tag.id.desc()],
        user=current_user,
    )
    return {'tag_list': [tag.to_dict() for tag in tag_list]}


@blueprint.post('/api/tags')
@login_required
def create_tag():
    tag = Tag.create(request.json['tag'], user=current_user)
    return {'tag': tag.to_dict()}


@blueprint.put('/api/tags/<string:tag_id>')
@login_required
def update_tag(tag_id: str):
    tag = Tag.get_or_404(tag_id)
    tag.verify_owner(current_user)
    tag.update(request.json['tag'])
    return {'tag': tag.to_dict()}


@blueprint.delete('/api/tags/<string:tag_id>')
@login_required
def delete_tag(tag_id: str):
    tag = Tag.get_or_404(tag_id)
    tag.verify_owner(current_user)
    tag.delete()
    return {'msg': '删除成功！'}
