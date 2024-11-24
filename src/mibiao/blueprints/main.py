from flask import Blueprint
from flask import render_template

from mibiao.models.domain import Domain
from mibiao.models.tag import Tag, DomainTag

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
    return render_template(
        'main/index.html',
        domain_list=domain_list,
    )


@blueprint.get('/<string:url_path_name>')
def index_by_tag(url_path_name: str):
    tag = Tag.get_one(Tag.url_path_name == url_path_name)
    if tag:
        domain_list = Domain.get_list(
            DomainTag.domain_id == Domain.id,
            DomainTag.tag_id == tag.id,
            Domain.is_hide == False,
            order_by=[
                Domain.rank,
                Domain.id.desc(),
            ],
        )
    else:
        domain_list = []
    return render_template(
        'main/index.html',
        domain_list=domain_list,
    )
