from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db

logger = logging.getLogger(__name__)
config = Config()


class ApplicationsView(web.View):
    @aiohttp_jinja2.template('apps/applications.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'deleted': None,
        }
        apps = db.session.query(db.Applications).filter_by(**filters).all()
        apps_data = [obj.to_json() for obj in apps]

        return {
            'applications': apps_data,
            "offers_types": avm.offers_types(),
            'active_menu_item': 'applications'
        }


class ApplicationsJsonView(web.View):
    async def get(self, *args, **kwargs):
        filters = {
            'deleted': None,
        }
        apps = db.session.query(db.Applications).filter_by(**filters).all()
        apps_data = [obj.to_json() for obj in apps]

        return web.json_response(apps_data, status=web.HTTPOk.status_code)
