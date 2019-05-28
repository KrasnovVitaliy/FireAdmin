from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm

logger = logging.getLogger(__name__)
config = Config()


class IndexView(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        return web.HTTPFound('/offers?offers_type=1')
        # return {
        #     "offers_types": avm.offers_types()
        # }
