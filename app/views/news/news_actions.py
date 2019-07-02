from aiohttp import web
import datetime
import logging
from config import Config
import views.all_view_methods as avm
import db

logger = logging.getLogger(__name__)
config = Config()


class NewsActionsView(web.View):
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        news = db.session.query(db.News).filter_by(**filters).first()
        if params['action'] == 'run':
            news.isActive = 1
        elif params['action'] == 'stop':
            news.isActive = 0
        elif params['action'] == 'delete':
            news.deleted = datetime.datetime.now()
        db.session.commit()

        return web.HTTPFound('news')


class NewsUpdateOrder(web.View):
    async def post(self, *args, **kwargs):
        params = self.request.rel_url.query
        data = await self.request.json()

        app_id = None
        if 'app_id' in params and params['app_id'] != None:
            app_id = params['app_id']

        for item in data:
            logger.debug("Post data: {}".format(item))
            news = db.session.query(db.NewsAppsRelations).filter_by(app_id=app_id, news_id=item['item_id']).first()
            news.position = item['position']

        db.session.commit()
        return web.HTTPOk()


class NewsUpdateComment(web.View):
    async def post(self, *args, **kwargs):
        data = await self.request.json()

        logger.debug("Post data: {}".format(data))
        offer = db.session.query(db.News).filter_by(id=data['item_id']).first()
        offer.comment = data['comment']

        db.session.commit()
        return web.HTTPOk()
