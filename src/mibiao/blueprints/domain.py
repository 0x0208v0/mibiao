from __future__ import annotations

import logging

from flask import Blueprint
from flask import request
from flask_login import login_required

from mibiao.models.domain import Domain

logger = logging.getLogger(__name__)

blueprint = Blueprint('domain', __name__)


@blueprint.get('/api/domains')
@login_required
def get_domain_list():
    domain_list = Domain.get_list(
        order_by=[Domain.is_hide, Domain.rank, Domain.id.desc()],
    )
    return {'domain_list': [domain.to_dict() for domain in domain_list]}


@blueprint.post('/api/domains')
@login_required
def create_domain():
    data = request.json['domain']
    domain = Domain.create(data)
    return {'domain': domain.to_dict()}


@blueprint.put('/api/domains/<string:domain_id>')
@login_required
def update_domain(domain_id: str):
    domain = Domain.get_or_404(domain_id)
    domain.update(request.json['domain'])
    return {'domain': domain.to_dict()}


@blueprint.delete('/api/domains/<string:domain_id>')
@login_required
def delete_domain(domain_id: str):
    domain = Domain.get_or_404(domain_id)
    domain.delete()
    return {'msg': '删除成功！'}
