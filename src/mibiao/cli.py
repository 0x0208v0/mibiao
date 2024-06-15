import os
import sys

import click


@click.group()
@click.option('--dry_run', type=bool, default=True)
@click.pass_context
def cli(ctx, dry_run: bool):
    ctx.ensure_object(dict)
    ctx.obj['dry_run'] = dry_run

    click.echo(f'os.getcwd()={os.getcwd()}')
    click.echo(f'sys.executable={sys.executable}')
    click.echo(f'dry_run={dry_run}')


@cli.command()
@click.pass_context
def task(ctx):
    from mibiao.tasks.start import main

    main()


if __name__ == '__main__':
    cli()
