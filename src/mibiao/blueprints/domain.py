import logging

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from mibiao.forms.domain import DomainForm
from mibiao.models import Domain

logger = logging.getLogger(__name__)

blueprint = Blueprint('domain', __name__)


@blueprint.get('/domain')
@login_required
def list():
    domain_list = Domain.get_list(
        Domain.user_id == current_user.id,
        order_by=[Domain.updated_at.desc()],
    )
    return render_template(
        'domain/list.html',
        domain_list=domain_list,
    )


@blueprint.route('/domain/create', methods=['GET', 'POST'])
@login_required
def create():
    form = DomainForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            form.flash_errors()
        else:
            domain = Domain(
                user_id=current_user.id,
                domain=form.domain.data,
                description=form.description.data,
                url=form.url.data,
                rank=form.rank.data,
                is_hide=form.is_hide.data,
            )
            domain.save()
            return redirect(url_for('domain.list'))

    return render_template('domain/create.html', form=form)


@blueprint.get('/domain/<string:id>')
@login_required
def detail(id: str):
    domain = Domain.get(id)
    if not domain or domain.user_id != current_user.id:
        return redirect(url_for('domain.list'))

    form = DomainForm(
        user_id=current_user.id,
        domain=domain.domain,
        description=domain.description,
        url=domain.url,
        rank=domain.rank,
        is_hide=domain.is_hide,
    )
    return render_template(
        'domain/detail.html',
        domain=domain,
        form=form,
    )


@blueprint.post('/domain/<string:id>')
@login_required
def update(id: str):
    domain = Domain.get(id)
    if not domain or domain.user_id != current_user.id:
        return redirect(url_for('domain.list'))

    form = DomainForm()
    if not form.validate_on_submit():
        form.flash_errors()
        return redirect(url_for('domain.list'))

    domain.domain = form.domain.data
    domain.description = form.description.data
    domain.url = form.url.data
    domain.rank = form.rank.data
    domain.is_hide = form.is_hide.data

    domain.save()
    flash('更新成功', 'success')
    return redirect(url_for('domain.list'))


@blueprint.route('/domain/<string:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id: str):
    domain = Domain.get(id)
    if not domain or domain.user_id != current_user.id:
        return redirect(url_for('domain.list'))

    domain.delete()
    flash('Domain已删除', 'success')
    return redirect(url_for('domain.list'))


@blueprint.get('/api/domains')
@login_required
def get_domain_list():
    domain_list = Domain.get_list(user=current_user, order_by=[Domain.rank, Domain.id.desc()])
    return {'domain_list': [domain.to_dict() for domain in domain_list]}


@blueprint.post('/api/domains')
@login_required
def create_domain():
    domain = Domain.create(request.json['domain'], user=current_user)
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
