from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db

logger = logging.getLogger(__name__)
config = Config()


class AppsOverviewView(web.View):
    @aiohttp_jinja2.template('apps/apps_overview.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        app = db.session.query(db.Applications).filter_by(**filters).first()
        app_data = app.to_json()

        return {
            'app': app_data,
            'offers_types': avm.offers_types(),
        }

    async def post(self, *args, **kwargs):
        params = self.request.rel_url.query
        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        filters = {
            'id': params['id']
        }

        app = db.session.query(db.Applications).filter_by(**filters).first()

        for field in post_data:
            setattr(app, field, post_data[field])

        db.session.add(app)
        db.session.commit()

        return web.HTTPFound('/applications?')
