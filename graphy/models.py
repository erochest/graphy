from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from graphy.db import Base


class AccountType:
    SAVINGS = 0
    CHECKING = 1
    CD = 2


account_beneficiaries = Table(
    'account_beneficiaries', Base.metadata,
    Column('account_id', ForeignKey('accounts.id'), primary_key=True),
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
)


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    owned_accounts = relationship(
        'Account',
        back_populates='owner',
    )
    beneficiaries_of = relationship(
        'Account',
        secondary=account_beneficiaries,
        back_populates='beneficiaries',
    )


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    number = Column(String(15), nullable=False, unique=True)
    account_type = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey('customers.id'))
    owner = relationship(
        Customer, back_populates='owned_accounts',
    )
    beneficiaries = relationship(
        Customer,
        secondary=account_beneficiaries,
        back_populates='beneficiaries_of',
    )
