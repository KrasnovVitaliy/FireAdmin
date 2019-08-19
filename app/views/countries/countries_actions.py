from aiohttp import web
import datetime
import logging
from config import Config
import db

logger = logging.getLogger(__name__)
config = Config()


class CountriesActionsView(web.View):
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        country = db.session.query(db.Countries).filter_by(**filters).delete()
        db.session.commit()
        return web.HTTPFound('/countries')
