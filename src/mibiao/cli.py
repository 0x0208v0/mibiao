import os
import sys

import click
import gunicorn.app.base

from mibiao.app import app
from mibiao.models.user import User
from mibiao.utils.password import random_password


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)

    click.echo('当前工作目录：')
    click.echo(os.getcwd())

    click.echo('Python可执行文件路径：')
    click.echo(sys.executable)


@cli.command()
@click.option('--host', default='0.0.0.0', help='要监听的主机名')
@click.option('--port', default='8080', help='要监听的端口号')
@click.pass_context
def run(ctx, host: str, port: int, workers: int = 1):
    click.echo('正在启动...')
    options = {
        'bind': '%s:%s' % (host, port),
        'workers': workers,
        'worker_class': 'gevent',
        'timeout': 5,
        'loglevel': 'INFO',
        'capture_output': True,
        'accesslog': '-',
        'errorlog': '-',
    }
    StandaloneApplication(app, options=options).run()


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
