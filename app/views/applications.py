from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db

logger = logging.getLogger(__name__)
config = Config()


class ApplicationsView(web.View):
    @aiohttp_jinja2.template('applications.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        apps = db.session.query(db.Applications).all()
        apps_data = [obj.to_json() for obj in apps]
        logger.debug("!!!!!!!")
        logger.debug(apps_data)

        return {
            'applications': apps_data,
            "offers_types": avm.offers_types()
        }
