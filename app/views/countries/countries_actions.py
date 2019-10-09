from aiohttp import web
import datetime
import logging
from config import Config
import db
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()


class CountriesActionsView(web.View):
    async def get(self, *args, **kwargs):
        user_permissions = await is_permitted(self.request, ['countries_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        country = db.session.query(db.Countries).filter_by(**filters).delete()
        db.session.commit()
        return web.HTTPFound('/countries')
