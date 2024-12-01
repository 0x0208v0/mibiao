from __future__ import annotations

import io
import zipfile

from flask import Blueprint
from flask import render_template
from flask import send_file
from flask_login import login_required

from mibiao.models.config import ConfigItem
from mibiao.models.domain import Domain
from mibiao.models.tag import DomainTag
from mibiao.models.tag import Tag
from mibiao.models.user import User

blueprint = Blueprint('admin', __name__)


@blueprint.get('/admin')
@login_required
def index():
    return render_template(
        'admin/index.html.j2',
    )


@blueprint.get('/api/export_data')
@login_required
def export_data():
    file = io.BytesIO()
    zip_file = zipfile.ZipFile(file, 'w')
    file_model_dict = {
        'user.json': User,
        'config_item.json': ConfigItem,
        'tag.json': Tag,
        'domain.json': Domain,
        'domain_tag.json': DomainTag,
    }
    for filename, model in file_model_dict.items():
        zip_file.writestr(filename, model.export_to_json_str())
    zip_file.close()
    file.seek(0)
    return send_file(file, as_attachment=True, download_name='data.zip')


@blueprint.post('/api/import_data')
@login_required
def import_data():
    return {}
