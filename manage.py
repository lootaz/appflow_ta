from flask import Flask
from flask_apscheduler import APScheduler
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from appflow_ta.api import api
from appflow_ta.commands import RunCommand
from appflow_ta.config import Config
from appflow_ta.models import db
from appflow_ta.schemas import ma


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())

    db.app = app
    db.init_app(app)

    Migrate(app, db)

    api.init_app(app)

    ma.init_app(app)

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    return app


app = create_app()

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('run', RunCommand)


if __name__ == '__main__':
    manager.run()


