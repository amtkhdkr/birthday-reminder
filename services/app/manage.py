import yaml
from flask.cli import FlaskGroup

from project import app_factory, db
from project.api.models import User

app = app_factory()
cli = FlaskGroup(create_app=app_factory)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db():
    """Seeds the database."""
    with open('initial_data.yml') as f:
        seed_users = yaml.safe_load(f)
        if 'avengers' not in seed_users:
            raise ValueError('Avengers not found in initial_data.yml')
    avengers = seed_users['avengers']
    for avenger_name, birthday in avengers.items():
        db.session.add(User(
            name=avenger_name,
            birthday=birthday
        ))
    db.session.commit()


if __name__ == '__main__':
    cli()
