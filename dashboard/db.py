from sqlalchemy import create_engine
from flask import current_app, g
from alembic import command
from alembic.config import Config
from flask_sqlalchemy import SQLAlchemy
from .models import *
import click

__all__ = ['get_db', 'close_db', 'init_db', 'init_db_command', 'init_app']

def get_db():
    if 'db' not in g:
        g.db = create_engine(current_app.config.get('SQLALCHEMY_DATABASE_URL'))

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.dispose()


def init_db():
    db = get_db()
    Base.metadata.create_all(db)
    alembic_cfg = Config(current_app.config.get('ALEMBIC_PATH'))
    command.stamp(alembic_cfg, "head")


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)