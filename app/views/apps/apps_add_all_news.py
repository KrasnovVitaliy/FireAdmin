from aiohttp import web
import logging
from config import Config
import db
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()


class AppsAddAllNewsView(web.View):
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])
        params = self.request.rel_url.query

        db.session.query(db.NewsAppsRelations).filter_by(app_id=params['id']).delete()

        news = db.session.query(db.News).all()
        for news_item in news:
            news_app_relation = db.NewsAppsRelations(app_id=params['id'], news_id=news_item.id)
            db.session.add(news_app_relation)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        return web.HTTPFound('/applications')


class AppsDeleteAllNewsView(web.View):
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query

        db.session.query(db.NewsAppsRelations).filter_by(app_id=params['id']).delete()

        return web.HTTPFound('/applications')
