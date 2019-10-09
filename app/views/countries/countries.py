from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()


class CountriesView(web.View):
    @aiohttp_jinja2.template('countries/countries.html')
    async def get(self, *args, **kwargs):
        user_permissions = await is_permitted(self.request, ['countries_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])


        params = self.request.rel_url.query

        countries = db.session.query(db.Countries).all()
        countries_data = [obj.to_json() for obj in countries]

        return {
            'countries': countries_data,
            "offers_types": avm.offers_types(),
            'active_menu_item': 'countries',
            "permissions": user_permissions,
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL
        }