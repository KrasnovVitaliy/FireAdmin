from aiohttp import web
import datetime
import logging
from config import Config
import views.all_view_methods as avm
import db

logger = logging.getLogger(__name__)
config = Config()


class AppsActionsView(web.View):
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        offer = db.session.query(db.Applications).filter_by(**filters).first()
        if params['action'] == 'delete':
            offer.deleted = datetime.datetime.now()
            db.session.commit()

        return web.HTTPFound('/applications')
