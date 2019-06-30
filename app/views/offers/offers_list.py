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

        try:
            current_app = int(params['current_app'])
        except Exception as e:
            current_app = None

        if current_app:
            results = db.session.query(db.OffersAppsRelations, db.Offers) \
                .filter(db.OffersAppsRelations.app_id == current_app) \
                .filter(db.OffersAppsRelations.offer_id == db.Offers.id) \
                .filter(db.Offers.deleted == None) \
                .filter(db.Offers.offer_type == filters['offer_type'])
            if 'isActive' in filters:
                results = results.filter(db.Offers.isActive == filters['isActive'])

            results = results.order_by(asc(db.OffersAppsRelations.position)).all()

            # Building offers list from results
            offers = [result[1] for result in results]

        else:
            offers = db.session.query(db.Offers).filter_by(**filters).order_by(asc(db.Offers.position)).all()

        offers_data = [obj.to_json() for obj in offers]

        apps = db.session.query(db.Applications).all()
        app_data = {}
        for app in apps:
            app_data[app.id] = app.to_json()

        for offer in offers_data:
            if 'related_apps' not in offer:
                offer['related_apps'] = []
            if 'app_position' not in offer:
                offer['app_position'] = {}

            offer_apps = db.session.query(db.OffersAppsRelations).filter_by(offer_id=offer['id']).all()
            for offer_app in offer_apps:
                offer['related_apps'].append(app_data[offer_app.app_id])
                offer['app_position'][offer_app.app_id] = offer_app.position

        filters = {
            'deleted': None,
        }
        apps = db.session.query(db.Applications).filter_by(**filters).all()
        apps_data = [obj.to_json() for obj in apps]

        if current_app:
            for app in apps_data:
                if app['id'] == int(current_app):
                    current_app = app
                    break

        logger.debug("Offers list get params: {}".format(params))

        return {
            'offers': offers_data,
            'offers_types': avm.offers_types(),
            'offers_type_id': int(params['offers_type']),
            'offers_state': offers_state,
            'active_menu_item': 'offers',
            'apps': apps_data,
            'current_app': current_app,
        }
