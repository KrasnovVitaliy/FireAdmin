from aiohttp import web
import datetime
import logging
from config import Config
import views.all_view_methods as avm
import db
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()


class AppsActionsView(web.View):
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        offer = db.session.query(db.Applications).filter_by(**filters).first()
        if params['action'] == 'delete':
            offer.deleted = datetime.datetime.now()
            try:
                db.session.commit()

            except Exception as e:
                logger.error("Can not create delete app record in db: {}".format(e.__str__()))
                db.session.rollback()

            return web.HTTPFound('/applications')

        if params['action'] == 'restore':
            offer.deleted = None
            try:
                db.session.commit()

            except Exception as e:
                logger.error("Can not restore deleted app record in db: {}".format(e.__str__()))
                db.session.rollback()

            return web.HTTPFound('/applications?is_deleted=true')
