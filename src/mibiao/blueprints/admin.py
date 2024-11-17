from flask import Blueprint
from flask import render_template
from flask_login import login_required

blueprint = Blueprint('admin', __name__)


@blueprint.get('/admin')
@login_required
def index():
    return render_template(
        'admin/index.html',
    )
