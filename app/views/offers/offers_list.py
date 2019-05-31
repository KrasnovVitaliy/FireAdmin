from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db
from sqlalchemy import asc

logger = logging.getLogger(__name__)
config = Config()


class OffersView(web.View):
    @aiohttp_jinja2.template('offers/offers.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'deleted': None,
            'offer_type': params['offers_type']
        }
        if 'state' in params:
            offers_state = params['state'].lower()
            if offers_state == 'active':
                filters['isActive'] = 1
            elif offers_state == 'inactive':
                filters['isActive'] = 0
        else:
            offers_state = 'all'

        offers = db.session.query(db.Offers).filter_by(**filters).order_by(asc(db.Offers.position)).all()
        offers_data = [obj.to_json() for obj in offers]

        apps = db.session.query(db.Applications).all()
        app_data = {}
        for app in apps:
            app_data[app.id] = app.to_json()

        for offer in offers_data:
            if 'related_apps' not in offer:
                offer['related_apps'] = []

            offer_apps = db.session.query(db.OffersAppsRelations).filter_by(offer_id=offer['id']).all()
            for offer_app in offer_apps:
                offer['related_apps'].append(app_data[offer_app.app_id])

        return {
            'offers': offers_data,
            'offers_types': avm.offers_types(),
            'offers_type_id': int(params['offers_type']),
            'offers_state': offers_state,
            'active_menu_item': 'offers'
        }
