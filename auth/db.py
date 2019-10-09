import datetime
from sqlalchemy import create_engine, Column, DateTime, Integer, String, func, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import Config

config = Config()

Base = declarative_base()

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(config.DB_URI))
session = scoped_session(Session)


class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    name = Column(String(50))
    apps_permission = Column(Boolean, default=False)
    offers_permission = Column(Boolean, default=False)
    offers_type_permission = Column(Boolean, default=False)
    news_permission = Column(Boolean, default=False)
    countries_permission = Column(Boolean, default=False)
    users_permission = Column(Boolean, default=False)
    journal_permission = Column(Boolean, default=False)
    deleted = Column(DateTime)

    def __init__(self, name=None, apps_permission=None, offers_permission=None, offers_type_permission=None,
                 news_permission=None,
                 countries_permission=None, users_permission=None, journal_permission=None):
        self.name = name
        self.apps_permission = apps_permission
        self.offers_permission = offers_permission
        self.offers_type_permission = offers_type_permission
        self.news_permission = news_permission
        self.countries_permission = countries_permission
        self.users_permission = users_permission
        self.journal_permission = journal_permission

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'update_date', 'name', 'apps_permission', 'offers_permission',
                        'offers_type_permission', 'news_permission', 'countries_permission', 'users_permission',
                        'journal_permission', 'deleted']
        return self.serialize(to_serialize)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    role = Column(Integer, ForeignKey("roles.id"))
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    pass_hash = Column(String(100))
    api_key = Column(String(50))
    deleted = Column(DateTime)

    def __init__(self, role=None, first_name='', last_name='', email='', pass_hash='', api_key=''):
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.pass_hash = pass_hash
        self.api_key = api_key

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'role', 'create_date', 'update_date', 'first_name', 'last_name', 'email', 'pass_hash',
                        'api_key',
                        'deleted']
        return self.serialize(to_serialize)


def prepare_db():
    engine = create_engine(config.DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    role = Roles(
        name='admin',
        apps_permission=True,
        offers_permission=True,
        offers_type_permission=True,
        news_permission=True,
        countries_permission=True,
        users_permission=True,
        journal_permission=True
    )
    session.add(role)

    role = Roles(
        name='user',
        apps_permission=True,
        offers_permission=True,
        offers_type_permission=False,
        news_permission=True,
        countries_permission=False,
        users_permission=False,
        journal_permission=False
    )
    session.add(role)

    role = Roles(
        name='manager',
        apps_permission=False,
        offers_permission=True,
        offers_type_permission=False,
        news_permission=True,
        countries_permission=False,
        users_permission=False,
        journal_permission=False
    )
    session.add(role)
    session.commit()


# creates database
if __name__ == "__main__":
    prepare_db()
