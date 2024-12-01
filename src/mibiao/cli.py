from __future__ import annotations

import os
import sys

import click

from mibiao.app import app
from mibiao.models.user import User
from mibiao.utils.password import random_password


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)

    click.echo('当前工作目录：')
    click.echo(os.getcwd())

    click.echo('Python可执行文件路径：')
    click.echo(sys.executable)


@cli.command()
@click.pass_context
def reset_password(ctx):
    click.echo('开始重置密码...')

    click.echo('请输入新密码: ')
    password = input()
    password = password.strip() if password else ''
    if not password:
        click.echo('没有输入密码，正在为你生成随机密码...')
        password = random_password()

    click.echo('新密码如下：')
    click.echo(password)

    with app.app_context():
        user = User.get_one_or_404()
        user.password = password or random_password()
        user.save()
    click.echo('密码已重置！')


if __name__ == '__main__':
    cli()
