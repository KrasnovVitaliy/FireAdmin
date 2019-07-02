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
    deleted = Column(DateTime)

    def __init__(self, name=None):
        self.name = name

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'update_date', 'name', 'deleted']
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
        to_serialize = ['id', 'role', 'create_date', 'update_date', 'first_name', 'last_name', 'email', 'pass_hash', 'api_key',
                        'deleted']
        return self.serialize(to_serialize)


def prepare_db():
    engine = create_engine(config.DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    for name in ['admin', 'user']:
        role = Roles(name=name)
        session.add(role)
        session.commit()


# creates database
if __name__ == "__main__":
    prepare_db()
