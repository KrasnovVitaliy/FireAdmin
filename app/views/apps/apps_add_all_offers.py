from aiohttp import web
import logging
from config import Config
import db
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()


class AppsAddAllOffersView(web.View):
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query

        db.session.query(db.OffersAppsRelations).filter_by(app_id=params['id']).delete()

        offers = db.session.query(db.Offers).all()
        for offer in offers:
            offer_app_relation = db.OffersAppsRelations(app_id=params['id'], offer_id=offer.id)
            db.session.add(offer_app_relation)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        return web.HTTPFound('/applications')


class AppsDeleteAllOffersView(web.View):
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query

        db.session.query(db.OffersAppsRelations).filter_by(app_id=params['id']).delete()

        return web.HTTPFound('/applications')
