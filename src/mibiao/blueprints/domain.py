import logging

from flask import Blueprint
from flask import request
from flask_login import current_user
from flask_login import login_required

from mibiao.models.domain import Domain

logger = logging.getLogger(__name__)

blueprint = Blueprint('domain', __name__)


@blueprint.get('/api/domains')
@login_required
def get_domain_list():
    domain_list = Domain.get_list(
        order_by=[Domain.is_hide, Domain.rank, Domain.id.desc()],
        user=current_user,
    )
    return {'domain_list': [domain.to_dict() for domain in domain_list]}


@blueprint.post('/api/domains')
@login_required
def create_domain():
    data = request.json['domain']
    domain = Domain.create(data, user=current_user)
    return {'domain': domain.to_dict()}


@blueprint.put('/api/domains/<string:domain_id>')
@login_required
def update_domain(domain_id: str):
    domain = Domain.get_or_404(domain_id)
    domain.verify_owner(current_user)
    domain.update(request.json['domain'])
    return {'domain': domain.to_dict()}


@blueprint.delete('/api/domains/<string:domain_id>')
@login_required
def delete_domain(domain_id: str):
    domain = Domain.get_or_404(domain_id)
    domain.verify_owner(current_user)
    domain.delete()
    return {'msg': '删除成功！'}
