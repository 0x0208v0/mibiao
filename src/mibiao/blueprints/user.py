from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Email

from mibiao.models import User


class BaseForm(FlaskForm):
    def flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash(f"{getattr(self, field).label.text}: {error}", 'error')


class LoginForm(BaseForm):
    email = StringField('邮箱：', validators=[DataRequired(), Email()])
    password = StringField('密码：', validators=[DataRequired()])
    remember_me = BooleanField('保持登陆')
    submit = SubmitField('登陆')


class RegisterForm(BaseForm):
    email = StringField('邮箱：', validators=[DataRequired(), Email()])
    password = StringField('密码：', validators=[DataRequired()])
    submit = SubmitField('注册')


blueprint = Blueprint('user', __name__, url_prefix='/')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user = User.login(email=form.email.data, password=form.password.data)
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('admin.index'))
            except ValueError as e:
                flash(f'{e}', 'error')
        else:
            form.flash_errors()
    return render_template('user/login.html', form=form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                User.register(email=form.email.data, password=form.password.data)
                flash('注册成功！', 'success')
                return redirect(url_for('user.login'))
            except ValueError as e:
                flash(f'{e}', 'error')
        else:
            form.flash_errors()
    return render_template('user/register.html', form=form)


@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@blueprint.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    current_user.delete()
    flash('账户已删除', 'success')
    return redirect(url_for('main.index'))


@blueprint.get('/api/users/me')
@login_required
def get_my_info():
    return {'user': current_user.to_dict()}


@blueprint.put('/api/users/me')
@login_required
def update_my_info():
    current_user.update(request.json['user'])
    return {'user': current_user.to_dict()}
