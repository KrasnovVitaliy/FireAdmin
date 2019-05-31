from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db

logger = logging.getLogger(__name__)
config = Config()


class AppsCreateView(web.View):
    @aiohttp_jinja2.template('apps/apps_create.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query
        return {
            'offers_types': avm.offers_types(),
        }

    async def post(self, *args, **kwargs):
        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        application = db.Applications()

        for field in post_data:
            setattr(application, field, post_data[field])

        db.session.add(application)
        db.session.commit()

        return web.HTTPFound('/applications?')
