from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db

logger = logging.getLogger(__name__)
config = Config()


class OffersOverviewView(web.View):
    @aiohttp_jinja2.template('offers/offers_overview.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        offer = db.session.query(db.Offers).filter_by(**filters).first()
        offer_data = offer.to_json()

        filters = {
            'deleted': None,
        }
        apps = db.session.query(db.Applications).filter_by(**filters).all()
        apps_data = [obj.to_json() for obj in apps]

        filters = {
            'offer_id': params['id']
        }

        offer_apps = db.session.query(db.OffersAppsRelations).filter_by(**filters).all()
        offer_apps_data = [obj.app_id for obj in offer_apps]

        return {
            'offers_types': avm.offers_types(),
            'offer': offer_data,
            'apps': apps_data,
            'offers_apps': offer_apps_data,
            'active_menu_item': 'offers',
            'offers_type_id': int(offer_data['offer_type']),
        }

    async def post(self, *args, **kwargs):
        params = self.request.rel_url.query

        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        filters = {
            'id': params['id']
        }
        offer = db.session.query(db.Offers).filter_by(**filters).first()

        for field in post_data:
            if "app_" in field:
                continue

            if field in ['isActive', 'mir', 'visa', 'mastercard', 'qiwi', 'yandex', 'cash']:
                setattr(offer, field, 1)
            else:
                setattr(offer, field, post_data[field])

        if 'isActive' not in post_data:
            setattr(offer, 'isActive', 0)

        # Update offers applications relation
        filters = {
            'offer_id': params['id']
        }
        db.session.query(db.OffersAppsRelations).filter_by(**filters).delete()

        logger.debug('!!!!!!')
        logger.debug(post_data)
        logger.debug('!!!!!!')
        for field in post_data:
            if "app_" in field:
                offer_app_relation = db.OffersAppsRelations(app_id=field.replace('app_', ''), offer_id=params['id'])
                db.session.add(offer_app_relation)

        db.session.commit()

        # return web.HTTPFound('offers_overview?id={}'.format(params['id']))
        return web.HTTPFound('/offers?offers_type={}'.format(offer.offer_type))
