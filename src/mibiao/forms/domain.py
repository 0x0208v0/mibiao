from wtforms import IntegerField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired

from mibiao.forms.base import BaseForm


class DomainForm(BaseForm):
    domain = StringField(
        '域名：',
        validators=[
            DataRequired(message='域名必填'),
        ],
        render_kw={
            'placeholder': '必填。如：woaimi.com',
        }
    )

    description = TextAreaField(
        '域名介绍：',
        render_kw={
            'rows': 5,
            'placeholder': '非必填。如：寓意为“我爱米”，原价220，续费123',
        }
    )

    rank = IntegerField(
        '排序值：',
        default=1,
        validators=[],
        render_kw={
            'placeholder': '非必填。如：首页的米表会按照“排序值”，从小带大排序',
        }
    )

    url = StringField(
        '示例网址：',
        validators=[],
        render_kw={
            'placeholder': '非必填。如：https://woaimi.com',
        }
    )

    is_hide = BooleanField(
        '是否隐藏：',
        default=False,
        render_kw={
            'placeholder': '如：首页的米表会按照“排序值”，从小带大排序',
        }
    )
