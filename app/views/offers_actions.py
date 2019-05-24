from aiohttp import web
import datetime
import logging
from config import Config
import views.all_view_methods as avm
import db

logger = logging.getLogger(__name__)
config = Config()


class OffersActionsView(web.View):
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        offer = db.session.query(db.Offers).filter_by(**filters).first()
        if params['action'] == 'run':
            offer.isActive = 1
        elif params['action'] == 'stop':
            offer.isActive = 0
        elif params['action'] == 'delete':
            offer.deleted = datetime.datetime.now()
        db.session.commit()

        return web.HTTPFound('offers?offers_type={}'.format(params['offer_type']))
