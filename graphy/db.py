from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker)


Base = declarative_base()

Session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False,
))


def init_app(app):
    engine = create_engine(
        app.config['DATABASE_URL'], echo=app.env == 'development',
    )
    Session.configure(bind=engine)
    Base.query = Session.query_property()
    Base.metadata.create_all(bind=engine)

    app.teardown_appcontext(shutdown_session)


def shutdown_session(exception=None):
    Session.remove()
