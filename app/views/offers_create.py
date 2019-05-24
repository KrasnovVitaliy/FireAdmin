from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db

logger = logging.getLogger(__name__)
config = Config()


class OffersCreateView(web.View):
    @aiohttp_jinja2.template('offers_create.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query
        offer_data = {}
        if 'offers_type' in params:
            offer_data['offer_type'] = int(params['offers_type'])

        apps = db.session.query(db.Applications).all()
        apps_data = [obj.to_json() for obj in apps]

        return {
            'apps': apps_data,
            'offers_types': avm.offers_types(),
            'offer': offer_data
        }

    async def post(self, *args, **kwargs):
        params = self.request.rel_url.query

        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        offer = db.Offers()

        for field in post_data:
            if field in ['isActive', 'mir', 'visa', 'mastercard', 'qiwi', 'yandex', 'cash']:
                setattr(offer, field, 1)
            else:
                setattr(offer, field, post_data[field])

        if 'isActive' not in post_data:
            setattr(offer, 'isActive', 0)

        db.session.add(offer)
        db.session.commit()

        # Update offers applications relation
        for field in post_data:
            if "app_" in field:
                offer_app_relation = db.OffersAppsRelations(app_id=field.replace('app_', ''), offer_id=offer.id)
                db.session.add(offer_app_relation)

        db.session.commit()

        return web.HTTPFound('/offers?offers_type={}'.format(offer.offer_type))
