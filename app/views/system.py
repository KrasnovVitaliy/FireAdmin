from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db
import os
import uuid
import json
import datetime

logger = logging.getLogger(__name__)
config = Config()


def process_offer(offer_type, offer_data):
    logger.debug('Process offer type: {} offer: {}'.format(offer_type, offer_data))

    offer = db.Offers()
    offer.offer_type = offer_type.id

    for field in offer_data:
        if field in ['isActive', 'mir', 'visa', 'mastercard', 'qiwi', 'yandex', 'cash']:
            setattr(offer, field, 1)
        elif field == 'order':
            setattr(offer, field, offer_data[field].split("?")[0])
        else:
            setattr(offer, field, offer_data[field])

    if 'isActive' not in offer_data:
        setattr(offer, 'isActive', 0)

    db.session.add(offer)
    db.session.commit()
    pass


def process_news(news_data):
    logger.debug('Process offer news: {}'.format(news_data))

    news = db.News()

    for field in news_data:
        if field in ['isActive', ]:
            setattr(news, field, 1)
        elif field == 'expireDate':
            expire_date = datetime.datetime.strptime(news_data[field], "%d.%m.%y")
            setattr(news, field, expire_date)
        else:
            setattr(news, field, news_data[field])

    if 'isActive' not in news_data:
        setattr(news, 'isActive', 0)

    db.session.add(news)
    db.session.commit()
    pass


def process_offer_type(offer_type_name):
    offer_type = db.session.query(db.OffersTypes).filter(db.OffersTypes.name == offer_type_name).first()
    if not offer_type:
        offer_type = db.OffersTypes(name=offer_type_name, description=offer_type_name)
        db.session.add(offer_type)
        db.session.commit()
    return offer_type


def process_saved_file(file_path):
    with open(file_path) as infile:
        offers_data = json.load(infile)
        logger.debug(offers_data)

        for offer in offers_data['news']:
            process_news(offer)

        for offer_type_name in offers_data.keys():
            if offer_type_name != 'news':
                logger.debug("Offer type name: {}".format(offer_type_name))
                offer_type = process_offer_type(offer_type_name=offer_type_name)
                if isinstance(offers_data[offer_type_name], list):
                    for offer in offers_data[offer_type_name]:
                        process_offer(offer_type, offer)


class SystemView(web.View):
    @aiohttp_jinja2.template('system.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        return {
            "offers_types": avm.offers_types(),
            'active_menu_item': 'system',
            'auth_service_address': config.AUTH_SERVICE_ADDRESS
        }

    async def post(self):
        reader = await self.request.multipart()
        while True:
            field = await reader.next()
            if not field:
                logger.debug('All files read')
                break

            if field.name == 'offers-json':
                logger.debug('Processing offers-json file')
                filename = field.filename
                logger.debug('Filename: {}'.format(filename))

                filename = uuid.uuid4().hex
                file_path = os.path.join(config.FILE_UPLOAD_PATH, filename)
                with open(file_path, 'wb') as f:
                    while True:
                        chunk = await field.read_chunk()  # 8192 bytes by default.
                        if not chunk:
                            break
                        f.write(chunk)
                logger.debug('File saved to {}'.format(file_path))
                process_saved_file(file_path=file_path)
                os.remove(file_path)

        return web.HTTPFound('/system')
