from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db

logger = logging.getLogger(__name__)
config = Config()


class CountriesCreateView(web.View):
    @aiohttp_jinja2.template('countries/countries_create.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query
        return {
            'auth_service_address': config.AUTH_SERVICE_ADDRESS
        }

    async def post(self, *args, **kwargs):
        params = self.request.rel_url.query
        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        country = db.Countries()
        for field in post_data:
            setattr(country, field, post_data[field])

        db.session.add(country)
        db.session.commit()
        return web.HTTPFound('/countries')
