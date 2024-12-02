from __future__ import annotations

import io
import zipfile

import pendulum
from flask import Blueprint
from flask import render_template
from flask import request
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


FILE_MODEL_DICT = {
    'user.json': User,
    'config_item.json': ConfigItem,
    'domain.json': Domain,
    'domain_tag.json': DomainTag,
    'tag.json': Tag,
}


@blueprint.get('/api/export-data')
@login_required
def export_data():
    file = io.BytesIO()
    zip_file = zipfile.ZipFile(file, 'w')

    for filename, model in FILE_MODEL_DICT.items():
        zip_file.writestr(filename, model.export_to_json_str())
    zip_file.close()
    file.seek(0)
    date_str = pendulum.now('Asia/Shanghai').strftime('%Y%m%d')
    download_name = f"data-{date_str}.zip"
    return send_file(
        file,
        as_attachment=True,
        download_name=download_name,
    )


@blueprint.post('/api/import-data')
@login_required
def import_data():
    file = request.files.get('file')
    if file:
        zip_file = zipfile.ZipFile(file.stream)
        filename_json_str_map = {}
        for filename in zip_file.namelist():
            if filename in FILE_MODEL_DICT:
                filename_json_str_map[filename] = zip_file.read(filename).decode('utf-8')
        for filename, model in FILE_MODEL_DICT.items():
            if filename in filename_json_str_map:
                FILE_MODEL_DICT[filename].delete_all()
        for filename, model in FILE_MODEL_DICT.items():
            if filename in filename_json_str_map:
                FILE_MODEL_DICT[filename].import_from_json_str(filename_json_str_map[filename])
    return {'ok': True}
