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


def populate():
    import os
    import random
    from faker import Faker
    from .models import Account, Customer

    class App:
        env = 'development'
        config = {
            'DATABASE_URL': os.getenv('DATABASE_URL')
        }

        def teardown_appcontext(self, fn):
            pass

    app = App()
    init_app(app)

    faker = Faker()
    n = 12

    session = Session()
    try:
        customers = []
        for _ in range(n):
            customer = Customer(name=faker.name())
            session.add(customer)
            customers.append(customer)
        for _ in range(n * 3):
            owner_index = random.randrange(n)
            bene_index = set()
            target_size = random.randrange(4)
            while len(bene_index) < target_size:
                i = random.randrange(len(customers))
                if i != owner_index:
                    bene_index.add(i)
            account = Account(
                number=faker.ean8(),
                account_type=random.randrange(3),
                owner=customers[owner_index],
                beneficiaries=[customers[i] for i in bene_index],
            )
            session.add(account)
    except:    # noqa: E722
        session.rollback()
        raise
    else:
        session.commit()


if __name__ == '__main__':
    populate()
