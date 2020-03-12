import json
import click
from models import Base, add_user, create_user_task
from flask.cli import FlaskGroup
from app import app

cli = FlaskGroup(app)

@cli.command('clear-db')
def clear_db():
    Base.metadata.drop_all()
    Base.metadata.create_all()

@cli.command('reset-db')
def reset_db():
    Base.metadata.drop_all()
    Base.metadata.create_all()
    with open('MOCK_DATA.json') as f:
        mock = json.load(f)
    for i in mock:
        add_user(**i)

@cli.command('fill-users')
def fill_db():
    with open('MOCK_DATA.json') as f:
        mock = json.load(f)
    for i in mock:
        add_user(**i)

@cli.command('add-access')
@click.argument('name')
def add_access(name):
    if name:
        print(name)
    else:
        print('Goodbye')

@cli.command('fill-tasks')
def fill_tasks():
    with open('MOCK_TASKS.json') as f:
        mock = json.load(f)
    for i in mock:
        create_user_task(**i)

cli()

# USAGE: python manage.py reset-db
# USAGE: python manage.py fill-users
# USAGE: python manage.py fill-tasks