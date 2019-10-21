from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()


class CountriesCreateView(web.View):
    @aiohttp_jinja2.template('countries/countries_create.html')
    async def get(self, *args, **kwargs):
        user_permissions = await is_permitted(self.request, ['countries_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])
        params = self.request.rel_url.query
        return {
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL,
            "permissions": user_permissions,
        }

    async def post(self, *args, **kwargs):
        user_permissions = await is_permitted(self.request, ['countries_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])
        params = self.request.rel_url.query
        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        country = db.Countries()
        for field in post_data:
            setattr(country, field, post_data[field])

        db.session.add(country)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return web.HTTPFound('/countries')
