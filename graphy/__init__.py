#!/usr/bin/env python


from flask import Flask


def create_app(config_filename=None):
    app = Flask(__name__)
    if config_filename is not None:
        app.config.from_pyfile(config_filename)

    from graphy import db
    db.init_app(app)

    return app
