from aiohttp import web
import logging
from config import Config
import db

logger = logging.getLogger(__name__)
config = Config()


class AppsAddAllOffersView(web.View):
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        db.session.query(db.OffersAppsRelations).filter_by(app_id=params['id']).delete()

        offers = db.session.query(db.Offers).all()
        for offer in offers:
            offer_app_relation = db.OffersAppsRelations(app_id=params['id'], offer_id=offer.id)
            db.session.add(offer_app_relation)
        db.session.commit()

        return web.HTTPFound('/applications')


class AppsDeleteAllOffersView(web.View):
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        db.session.query(db.OffersAppsRelations).filter_by(app_id=params['id']).delete()

        return web.HTTPFound('/applications')
