from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db
from sqlalchemy import asc
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()


class OffersView(web.View):
    def filter_offers_by_countries(self, offers, country_id):
        offers_list = []
        for offer in offers:
            result = db.session.query(db.OffersCountriesRelations) \
                .filter(db.OffersCountriesRelations.offer_id == offer.id) \
                .filter(db.OffersCountriesRelations.country_id == country_id).first()

            if result:
                offers_list.append(offer)

        return offers_list

    def get_offer_country_position(self, offer_id, country_id, app_id):
        offer_position = db.session.query(db.OffersAppsCountriesPositions) \
            .filter(db.OffersAppsCountriesPositions.offer_id == offer_id) \
            .filter(db.OffersAppsCountriesPositions.country_id == country_id) \
            .filter(db.OffersAppsCountriesPositions.app_id == app_id).first()

        if offer_position:
            return offer_position.position
        return 0

    @aiohttp_jinja2.template('offers/offers.html')
    async def get(self, *args, **kwargs):
        user_permissions = await is_permitted(self.request, ['offers_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

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

        try:
            current_country = int(params['current_country'])
        except Exception as e:
            current_country = None

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

        if current_country:
            offers = self.filter_offers_by_countries(offers, current_country)

        offers_data = [obj.to_json() for obj in offers]

        apps = db.session.query(db.Applications).all()
        app_data = {}
        for app in apps:
            app_data[app.id] = app.to_json()

        for offer in offers_data:
            if 'related_apps' not in offer:
                offer['related_apps'] = []
            if 'app_position' not in offer:
                offer['app_position'] = 0

            offer_apps = db.session.query(db.OffersAppsRelations).filter_by(offer_id=offer['id']).all()
            for offer_app in offer_apps:
                offer['related_apps'].append(app_data[offer_app.app_id])

                if current_app:
                    if current_country:
                        offer['app_position'] = self.get_offer_country_position(
                            offer_id=offer['id'], country_id=current_country, app_id=current_app)
                    else:
                        offer['app_position'] = self.get_offer_country_position(
                            offer_id=offer['id'], country_id=-1, app_id=current_app)

                        if not offer['app_position']:
                            offer['app_position'] = 0
                else:
                    offer['app_position'] = 0

        offers_data = sorted(offers_data, key=lambda k: k['app_position'])
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

        countries = db.session.query(db.Countries).all()
        countries_data = [obj.to_json() for obj in countries]

        if current_country:
            for country in countries_data:
                if country['id'] == int(current_country):
                    current_country = country
                    break

        return {
            'offers': offers_data,
            'offers_types': avm.offers_types(),
            "permissions": user_permissions,
            'offers_type_id': int(params['offers_type']),
            'offers_state': offers_state,
            'active_menu_item': 'offers',
            'apps': apps_data,
            'current_app': current_app,
            'countries': countries_data,
            'current_country': current_country,
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL
        }
