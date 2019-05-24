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


class Applications(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    name = Column(String(50))
    description = Column(String(100))
    fb_link = Column(String(200))
    appmetrica_link = Column(String(200))
    fabrica_link = Column(String(200))
    appsflyer_link = Column(String(200))
    creator = Column(Integer)
    deleted = Column(DateTime)

    def __init__(self, name=None, description=None, fb_link=None, appmetrica_link=None, fabrica_link=None,
                 appsflyer_link=None):
        self.name = name
        self.description = description
        self.fb_link = fb_link
        self.appmetrica_link = appmetrica_link
        self.fabrica_link = fabrica_link
        self.appsflyer_link = appsflyer_link

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'update_date', 'name', 'description', 'fb_link', 'appmetrica_link',
                        'fabrica_link', 'appsflyer_link', 'creator', 'deleted']
        return self.serialize(to_serialize)


class OffersTypes(Base):
    __tablename__ = 'offers_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(String(200))
    deleted = Column(DateTime)

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'name', 'description']
        return self.serialize(to_serialize)


class Offers(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    offer_type = Column(Integer, ForeignKey("offers_types.id"))

    isActive = Column(Integer)
    itemId = Column(Integer)
    name = Column(String(200))
    description = Column(String(1000))

    order = Column(String(200))
    orderButtonText = Column(String(50))

    percent = Column(String(50))
    percentPostfix = Column(String(50))
    percentPrefix = Column(String(50))

    score = Column(Integer)
    screen = Column(String(200))
    summ = Column(String(200))
    term = Column(String(200))

    mastercard = Column(Boolean)
    mir = Column(Boolean)
    visa = Column(Boolean)
    qiwi = Column(Boolean)
    yandex = Column(Boolean)
    cash = Column(Boolean)

    creator = Column(Integer)
    deleted = Column(DateTime)

    def __init__(self, offer_type=None, isActive=None, itemId=None,
                 name=None, description=None, order=None, orderButtonText=None, percent=None, percentPostfix=None,
                 percentPrefix=None, score=None, screen=None, summ=None, term=None, mastercard=None, mir=None,
                 visa=None, qiwi=None, yandex=None, cash=None):
        self.offer_type = offer_type
        self.isActive = isActive
        self.itemId = itemId
        self.name = name
        self.description = description
        self.order = order
        self.orderButtonText = orderButtonText
        self.percent = percent
        self.percentPostfix = percentPostfix
        self.percentPrefix = percentPrefix
        self.score = score
        self.screen = screen
        self.summ = summ
        self.term = term
        self.mastercard = mastercard
        self.mir = mir
        self.visa = visa
        self.qiwi = qiwi
        self.yandex = yandex
        self.cash = cash

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'update_date', 'offer_type', 'isActive', 'itemId',
                        'name', 'description', 'order', 'orderButtonText', 'percent', 'percentPostfix',
                        'percentPrefix', 'score', 'screen', 'summ', 'term', 'mastercard', 'mir',
                        'visa', 'qiwi', 'yandex', 'cash', 'creator']
        return self.serialize(to_serialize)


class OffersAppsRelations(Base):
    __tablename__ = 'offers_apps_relations'
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    app_id = Column(Integer, ForeignKey("applications.id"))

    def __init__(self, offer_id=None, app_id=None):
        self.offer_id = offer_id
        self.app_id = app_id

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'offer_id', 'app_id']
        return self.serialize(to_serialize)


def prepare_db():
    engine = create_engine(config.DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    for item in [
        {'name': 'cards_credit', 'description': 'Кредитные карты'},
        {'name': 'cards_debit', 'description': 'Дебитовые карты'},
        {'name': 'cards_installment', 'description': 'Карты рассрочки'},
        {'name': 'credits', 'description': 'Кредиты'},
        {'name': 'history', 'description': 'Кредитная история'},
        {'name': 'loans', 'description': 'Займы'},
        {'name': 'news', 'description': 'Новости'}]:
        offer_type = OffersTypes(name=item['name'], description=item['description'])
        session.add(offer_type)
        session.commit()

    # Just for test
    offer = Offers(name='Offer 1', offer_type=1, isActive=False,
                   screen='https://firebasestorage.googleapis.com/v0/b/ru-finance-credits.appspot.com/o/credit_cards%2Falfa-cash-back.png?alt=media&token=42bd01c6-a91e-4345-881b-5a9d1ff1c6fa')
    session.add(offer)

    offer = Offers(name='Offer 2', offer_type=1, isActive=True,
                   screen='https://firebasestorage.googleapis.com/v0/b/ru-finance-credits.appspot.com/o/credit_cards%2Falfa-cash-back.png?alt=media&token=42bd01c6-a91e-4345-881b-5a9d1ff1c6fa')
    session.add(offer)

    app = Applications(name="Даем заем", description="Jgbcfybt", fb_link=None, appmetrica_link=None, fabrica_link=None,
                       appsflyer_link=None)
    session.add(app)
    app = Applications(name="Займы под 0", description="Jgbcfybt", fb_link=None, appmetrica_link=None,
                       fabrica_link=None,
                       appsflyer_link=None)
    session.add(app)

    app = Applications(name="Выручайка", description="Jgbcfybt", fb_link=None, appmetrica_link=None,
                       fabrica_link=None,
                       appsflyer_link=None)
    session.add(app)

    session.commit()


if __name__ == "__main__":
    prepare_db()
