from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import db
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()


class OffersTypesView(web.View):
    @aiohttp_jinja2.template('offers/offers_types.html')
    async def get(self, *args, **kwargs):
        user_permissions = await is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])
        params = self.request.rel_url.query

        offers_types = db.session.query(db.OffersTypes).filter(db.OffersTypes.deleted == None).all()
        offers_types_data = [obj.to_json() for obj in offers_types]

        return {
            "permissions": user_permissions,
            'offers_types': offers_types_data,
            'active_menu_item': 'offers_types',
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL
        }
