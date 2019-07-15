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
    fb_id = Column(String(200))
    fb_url = Column(String(200))
    appmetrica_link = Column(String(200))
    fabrica_link = Column(String(200))
    appsflyer_link = Column(String(200))
    order_tracking_source = Column(String(50))
    license_term = Column(String(5000))
    creator = Column(Integer)
    deleted = Column(DateTime)

    def __init__(self, name=None, description=None, fb_id=None, fb_url=None, appmetrica_link=None, fabrica_link=None,
                 appsflyer_link=None, order_tracking_source=None, license_term=None):
        self.name = name
        self.description = description
        self.fb_id = fb_id
        self.fb_url = fb_url
        self.appmetrica_link = appmetrica_link
        self.fabrica_link = fabrica_link
        self.appsflyer_link = appsflyer_link
        self.order_tracking_source = order_tracking_source
        self.license_term = license_term

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'update_date', 'name', 'description', 'fb_id', 'fb_url', 'appmetrica_link',
                        'fabrica_link', 'appsflyer_link', 'order_tracking_source', 'license_term', 'creator',
                        'deleted']
        return self.serialize(to_serialize)


class OffersTypes(Base):
    __tablename__ = 'offers_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(String(200))
    deleted = Column(DateTime)

    def __init__(self, name=None, description=None, deleted=None):
        self.name = name
        self.description = description
        self.deleted = deleted

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
    itemId = Column(String(100))
    name = Column(String(200))
    description = Column(String(1000))

    order = Column(String(200))
    orderButtonText = Column(String(50))

    percent = Column(String(50))
    percentPostfix = Column(String(50))
    percentPrefix = Column(String(50))

    score = Column(Integer)
    screen = Column(String(200))

    summPrefix = Column(String(50))
    summMin = Column(String(50))
    summMid = Column(String(50))
    summMax = Column(String(50))
    summPostfix = Column(String(50))

    termMin = Column(String(50))
    termMax = Column(String(50))
    termMid = Column(String(50))
    termPrefix = Column(String(50))
    termPostfix = Column(String(50))

    mastercard = Column(Boolean)
    mir = Column(Boolean)
    visa = Column(Boolean)
    qiwi = Column(Boolean)
    yandex = Column(Boolean)
    cash = Column(Boolean)

    greenStickerText = Column(String(50))
    blueStickerText = Column(String(50))
    redStickerText = Column(String(50))

    position = Column(Integer)
    comment = Column(String(500))

    creator = Column(Integer)
    deleted = Column(DateTime)

    def __init__(self, offer_type=None, isActive=None, itemId=None,
                 name=None, description=None, order=None, orderButtonText=None, percent=None, percentPostfix=None,
                 percentPrefix=None, score=None, screen=None, mastercard=None, mir=None,
                 visa=None, qiwi=None, yandex=None, cash=None, greenStickerText=None, blueStickerText=None,
                 redStickerText=None, position=None, comment=None, termPostfix=None, termMax=None, termMid=None,
                 termMin=None, termPrefix=None, summPostfix=None, summPrefix=None, summMin=None, summMax=None,
                 summMid=None):
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
        self.mastercard = mastercard
        self.mir = mir
        self.visa = visa
        self.qiwi = qiwi
        self.yandex = yandex
        self.cash = cash
        self.greenStickerText = greenStickerText
        self.blueStickerText = blueStickerText
        self.redStickerText = redStickerText
        self.position = position
        self.comment = comment
        self.termPostfix = termPostfix
        self.termMax = termMax
        self.termMid = termMid
        self.termMin = termMin
        self.termPrefix = termPrefix
        self.summPrefix = summPrefix
        self.summMin = summMin
        self.summMid = summMid
        self.summMax = summMax
        self.summPostfix = summPostfix

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
                        'percentPrefix', 'score', 'screen', 'mastercard', 'mir',
                        'visa', 'qiwi', 'yandex', 'cash', 'creator', 'greenStickerText', 'blueStickerText',
                        'redStickerText', 'deleted', 'position', 'comment', 'termPostfix', 'termMax', 'termMid',
                        'termMin', 'termPrefix', 'summPostfix', 'summPrefix', 'summMin', 'summMax', 'summMid']
        return self.serialize(to_serialize)


class OffersAppsCountriesPositions(Base):
    __tablename__ = 'offers_apps_countries_positions'
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    offer_type_id = Column(Integer, ForeignKey("offers_types.id"))
    app_id = Column(Integer, ForeignKey("applications.id"))
    country_id = Column(Integer, ForeignKey("countries.id"))
    position = Column(Integer)

    def __init__(self, offer_id=None, app_id=None, offer_type_id=None, country_id=None, position=None):
        self.offer_id = offer_id
        self.app_id = app_id
        self.offer_type_id = offer_type_id
        self.country_id = country_id
        self.position = position

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'offer_id', 'offer_type_id', 'app_id', 'country_id', 'position']
        return self.serialize(to_serialize)


class NewsAppsCountriesPositions(Base):
    __tablename__ = 'news_apps_countries_positions'
    id = Column(Integer, primary_key=True)
    news_id = Column(Integer, ForeignKey("news.id"))
    app_id = Column(Integer, ForeignKey("applications.id"))
    country_id = Column(Integer, ForeignKey("countries.id"))
    position = Column(Integer)

    def __init__(self, news_id=None, app_id=None, country_id=None, position=None):
        self.news_id = news_id
        self.app_id = app_id
        self.country_id = country_id
        self.position = position

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'news_id', 'app_id', 'country_id', 'position']
        return self.serialize(to_serialize)


class OffersAppsRelations(Base):
    __tablename__ = 'offers_apps_relations'
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    app_id = Column(Integer, ForeignKey("applications.id"))
    position = Column(Integer)

    def __init__(self, offer_id=None, app_id=None, position=None):
        self.offer_id = offer_id
        self.app_id = app_id
        self.position = position

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'offer_id', 'app_id', 'position']
        return self.serialize(to_serialize)


class OffersAppsOrderUrls(Base):
    __tablename__ = 'offers_apps_order_urls'
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    app_id = Column(Integer, ForeignKey("applications.id"))
    order_url = Column(String(200))

    def __init__(self, offer_id=None, app_id=None, order_url=None):
        self.offer_id = offer_id
        self.app_id = app_id
        self.order_url = order_url

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'offer_id', 'app_id', 'order_url']
        return self.serialize(to_serialize)


class OffersAppsNames(Base):
    __tablename__ = 'offers_apps_order_names'
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    app_id = Column(Integer, ForeignKey("applications.id"))
    name = Column(String(200))

    def __init__(self, offer_id=None, app_id=None, name=None):
        self.offer_id = offer_id
        self.app_id = app_id
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
        to_serialize = ['id', 'offer_id', 'app_id', 'name']
        return self.serialize(to_serialize)


class OffersAppsCreatives(Base):
    __tablename__ = 'offers_apps_creatives'
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    app_id = Column(Integer, ForeignKey("applications.id"))
    creative_url = Column(String(200))

    def __init__(self, offer_id=None, app_id=None, creative_url=None):
        self.offer_id = offer_id
        self.app_id = app_id
        self.creative_url = creative_url

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'offer_id', 'app_id', 'creative_url']
        return self.serialize(to_serialize)


class OffersAppsTerms(Base):
    __tablename__ = 'offers_apps_terms'
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    app_id = Column(Integer, ForeignKey("applications.id"))
    termPostfix = Column(String(50))
    termMax = Column(String(50))
    termMid = Column(String(50))
    termMin = Column(String(50))
    termPrefix = Column(String(50))

    def __init__(self, offer_id=None, app_id=None, termPostfix=None, termMax=None, termMid=None,
                 termMin=None, termPrefix=None):
        self.offer_id = offer_id
        self.app_id = app_id
        self.termPostfix = termPostfix
        self.termMax = termMax
        self.termMid = termMid
        self.termMin = termMin
        self.termPrefix = termPrefix

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'offer_id', 'app_id', 'termPostfix', 'termMax', 'termMid', 'termMin',
                        'termPrefix']
        return self.serialize(to_serialize)


class OffersAppsSumms(Base):
    __tablename__ = 'offers_apps_summs'
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    app_id = Column(Integer, ForeignKey("applications.id"))
    summPostfix = Column(String(50))
    summMax = Column(String(50))
    summMid = Column(String(50))
    summMin = Column(String(50))
    summPrefix = Column(String(50))

    def __init__(self, offer_id=None, app_id=None, summPostfix=None, summMax=None, summMid=None,
                 summMin=None, summPrefix=None):
        self.offer_id = offer_id
        self.app_id = app_id
        self.summPostfix = summPostfix
        self.summMax = summMax
        self.summMid = summMid
        self.summMin = summMin
        self.summPrefix = summPrefix

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'offer_id', 'app_id', 'summPostfix', 'summMax', 'summMid', 'summMin',
                        'summPrefix']
        return self.serialize(to_serialize)


class OffersAppsPercents(Base):
    __tablename__ = 'offers_apps_percents'
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    app_id = Column(Integer, ForeignKey("applications.id"))
    percent = Column(String(50))
    percentPostfix = Column(String(50))
    percentPrefix = Column(String(50))

    def __init__(self, offer_id=None, app_id=None, percentPostfix=None, percent=None, percentPrefix=None):
        self.offer_id = offer_id
        self.app_id = app_id
        self.percentPostfix = percentPostfix
        self.percent = percent
        self.percentPrefix = percentPrefix

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'offer_id', 'app_id', 'percentPostfix', 'percent', 'percentPrefix']
        return self.serialize(to_serialize)


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    title = Column(String(200))
    itemId = Column(String(100))
    description = Column(String(200))
    expireDate = Column(DateTime)
    image = Column(String(200))
    isActive = Column(Integer)
    link = Column(String(500))
    deleted = Column(DateTime)
    position = Column(Integer)
    comment = Column(String(500))

    def __init__(self, title=None, description=None, expireDate=None, image=None, isActive=None, link=None,
                 itemId=None, position=None, comment=None):
        self.title = title
        self.description = description
        self.expireDate = expireDate
        self.image = image
        self.isActive = isActive
        self.link = link
        self.itemId = itemId
        self.position = position
        self.comment = comment

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                if attr_name == 'expireDate':
                    attr_value = attr_value.strftime("%d.%m.%Y")
                else:
                    attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'update_date', 'title', 'description', 'expireDate', 'image', 'isActive',
                        'link', 'deleted', 'itemId', 'position', 'comment']
        return self.serialize(to_serialize)


class NewsAppsRelations(Base):
    __tablename__ = 'news_apps_relations'
    id = Column(Integer, primary_key=True)
    news_id = Column(Integer, ForeignKey("news.id"))
    app_id = Column(Integer, ForeignKey("applications.id"))
    position = Column(Integer)

    def __init__(self, news_id=None, app_id=None, position=None):
        self.news_id = news_id
        self.app_id = app_id
        self.position = position

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'news_id', 'app_id', 'position']
        return self.serialize(to_serialize)


class Countries(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    code = Column(String(2))

    def __init__(self, name=None, code=None):
        self.name = name
        self.code = code

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'name', 'code']
        return self.serialize(to_serialize)


class OffersCountriesRelations(Base):
    __tablename__ = 'offers_countries_relations'
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    country_id = Column(Integer, ForeignKey("countries.id"))

    def __init__(self, offer_id=None, country_id=None):
        self.offer_id = offer_id
        self.country_id = country_id

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'offer_id', 'country_id']
        return self.serialize(to_serialize)


class NewsCountriesRelations(Base):
    __tablename__ = 'news_countries_relations'
    id = Column(Integer, primary_key=True)
    news_id = Column(Integer, ForeignKey("news.id"))
    country_id = Column(Integer, ForeignKey("countries.id"))

    def __init__(self, news_id=None, country_id=None):
        self.news_id = news_id
        self.country_id = country_id

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'news_id', 'country_id']
        return self.serialize(to_serialize)


class AppsCountriesTerms(Base):
    __tablename__ = 'apps_countries_terms'
    id = Column(Integer, primary_key=True)
    license_term = Column(String(5000))
    app_id = Column(Integer, ForeignKey("applications.id"))
    country_id = Column(Integer, ForeignKey("countries.id"))

    def __init__(self, app_id=None, country_id=None, license_term=None):
        self.app_id = app_id
        self.country_id = country_id
        self.license_term = license_term

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'app_id', 'country_id', 'license_term']
        return self.serialize(to_serialize)


class AppsCountriesRelations(Base):
    __tablename__ = 'apps_countries_relations'
    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey("applications.id"))
    country_id = Column(Integer, ForeignKey("countries.id"))

    def __init__(self, app_id=None, country_id=None, ):
        self.app_id = app_id
        self.country_id = country_id

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'app_id', 'country_id']
        return self.serialize(to_serialize)


def prepare_db():
    engine = create_engine(config.DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    prepare_db()
