from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db

logger = logging.getLogger(__name__)
config = Config()


class CountriesOverviewView(web.View):
    @aiohttp_jinja2.template('countries/countries_overview.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        country = db.session.query(db.Countries).filter_by(**filters).first()
        country_data = country.to_json()

        return {
            'country': country_data,
            'auth_service_address': config.AUTH_SERVICE_ADDRESS
        }

    async def post(self, *args, **kwargs):
        params = self.request.rel_url.query
        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        filters = {
            'id': params['id']
        }
        #
        country = db.session.query(db.Countries).filter_by(**filters).first()
        for field in post_data:
            setattr(country, field, post_data[field])

        db.session.commit()
        return web.HTTPFound('/countries')
