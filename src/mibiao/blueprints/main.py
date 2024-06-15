from flask import Blueprint
from flask import render_template

from mibiao.models.domain import Domain

blueprint = Blueprint('main', __name__, url_prefix='/')


@blueprint.get('/health')
def health():
    return 'ok'


@blueprint.get('/')
def index():
    domain_list = Domain.get_list(
        Domain.is_hide == False,
        order_by=[
            Domain.rank.desc(),
            Domain.id.desc(),
        ],
    )
    return render_template(
        'main/index.html',
        domain_list=domain_list,
    )
