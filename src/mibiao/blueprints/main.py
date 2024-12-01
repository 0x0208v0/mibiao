from __future__ import annotations

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for

from mibiao.models.domain import Domain
from mibiao.models.tag import DomainTag
from mibiao.models.tag import Tag
from mibiao.models.user import User

blueprint = Blueprint('main', __name__, url_prefix='/')


@blueprint.get('/health')
def health():
    return 'ok'


@blueprint.get('/')
def index():
    if not User.get_one():
        return redirect(url_for('user.register'))

    domain_list = Domain.get_list(
        Domain.is_hide.op('==')(False),
        order_by=[
            Domain.rank,
            Domain.id.desc(),
        ],
    )
    return render_template(
        'main/index.html.j2',
        domain_list=domain_list,
    )


@blueprint.get('/<string:url_path_name>')
def tag_index(url_path_name: str):
    if not User.get_one():
        return redirect(url_for('user.register'))

    tag = Tag.get_one(Tag.url_path_name == url_path_name)
    if tag:
        domain_list = Domain.get_list(
            DomainTag.domain_id == Domain.id,
            DomainTag.tag_id == tag.id,
            Domain.is_hide.op('==')(False),
            order_by=[
                Domain.rank,
                Domain.id.desc(),
            ],
        )
    else:
        domain_list = []
    return render_template(
        'main/index.html.j2',
        domain_list=domain_list,
    )
