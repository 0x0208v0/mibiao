from flask import Blueprint
from flask import render_template

from mibiao.models.domain import Domain
from mibiao.models.tag import Tag

blueprint = Blueprint('main', __name__, url_prefix='/')


@blueprint.get('/health')
def health():
    return 'ok'


@blueprint.get('/')
def index():
    domain_list = Domain.get_list(
        Domain.is_hide == False,
        order_by=[
            Domain.rank,
            Domain.id.desc(),
        ],
    )
    tag_list = Tag.get_list(
        Tag.is_hide == False,
        order_by=[
            Tag.rank,
            Tag.id.desc(),
        ],
    )
    return render_template(
        'main/index.html',
        domain_list=domain_list,
        tag_list=tag_list,
    )
