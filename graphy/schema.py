import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
from promise import Promise
from promise.dataloader import DataLoader

from .db import Session
from .models import (
    Customer as CustomerModel, Account as AccountModel, AccountType,
)


class CustomerLoader(DataLoader):

    def batch_load_fn(self, keys):
        session = Session()
        query = session.query(CustomerModel).filter(CustomerModel.id.in_(keys))
        customers = {
            customer.id: customer
            for customer in query.all()
        }
        return Promise.resolve(
            [customers.get(customer_id) for customer_id in keys],
        )


class Customer(SQLAlchemyObjectType):
    class Meta:
        model = CustomerModel
        interfaces = (relay.Node,)


class CustomerRelayConnection(relay.Connection):
    class Meta:
        node = Customer


# Global. Yeck. There must be a better way.
customer_loader = CustomerLoader()


class Account(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)

    number = graphene.String()
    account_type = graphene.Enum.from_enum(AccountType)
    owner = graphene.Field(Customer)
    beneficiaries = SQLAlchemyConnectionField(CustomerRelayConnection)

    def resolve_owner(self, info):
        return customer_loader.load(self.owner_id)


class AccountRelayConnection(relay.Connection):
    class Meta:
        node = Account


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_customers = SQLAlchemyConnectionField(CustomerRelayConnection)
    all_accounts = relay.ConnectionField(AccountRelayConnection)

    def resolve_all_accounts(self, info):
        session = Session()
        accounts = session.query(AccountModel).all()
        return accounts


schema = graphene.Schema(query=Query)


def init_app(app):
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True,
        )
    )
