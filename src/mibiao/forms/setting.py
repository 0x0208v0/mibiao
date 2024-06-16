from wtforms.fields.simple import StringField

from mibiao.forms.base import BaseForm


class SettingForm(BaseForm):
    name = StringField(
        '用户名：',
        validators=[],
        render_kw={
            'placeholder': '如：我爱米',
        }
    )

    avatar_url = StringField(
        '头像：',
        validators=[],
        render_kw={
            'placeholder': '必填。如：https://www.nodeseek.com/avatar/16798.png',
        }
    )
