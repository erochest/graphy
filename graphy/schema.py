import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView

from .models import (
    Customer as CustomerModel, Account as AccountModel,
)


class Customer(SQLAlchemyObjectType):
    class Meta:
        model = CustomerModel
        interfaces = (relay.Node,)


class CustomerRelayConnection(relay.Connection):
    class Meta:
        node = Customer


class Account(SQLAlchemyObjectType):
    class Meta:
        model = AccountModel
        interfaces = (relay.Node,)


class AccountRelayConnection(relay.Connection):
    class Meta:
        node = Account


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_customers = SQLAlchemyConnectionField(CustomerRelayConnection)
    all_accounts = SQLAlchemyConnectionField(AccountRelayConnection)


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
