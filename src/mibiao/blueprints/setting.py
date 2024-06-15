from flask import Blueprint
from flask import render_template
from flask_login import login_required

blueprint = Blueprint('setting', __name__)


@blueprint.get('/setting')
@login_required
def index():
    return render_template(
        'setting/index.html',
    )
