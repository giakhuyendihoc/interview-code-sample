from importlib import import_module

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from ._config import config
from .commons.error_handlers import register_error_handlers

app = Flask(__name__)
app.config.from_object(config)
app.config["MYSQL_DATABASE_CHARSET"] = "utf8mb4"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)


def register_subpackages():
    from main import models

    for m in models.__all__:
        import_module("main.models." + m)

    import main.controllers  # noqa


register_subpackages()
register_error_handlers(app)
