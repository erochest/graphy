#!/usr/bin/env python


import os
from flask import Flask


def create_app(config_filename=None):
    app = Flask(__name__)
    if config_filename is not None:
        app.config.from_pyfile(config_filename)
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

    from graphy import db
    from graphy import models as _models    # noqa: F401
    db.init_app(app)

    from graphy import schema
    schema.init_app(app)

    return app
