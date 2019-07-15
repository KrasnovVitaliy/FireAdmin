from aiohttp import web
import datetime
import logging
from config import Config
import views.all_view_methods as avm
import db
import utils.firebase_client as fb_client

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

        country_id = None
        if 'country_id' in params and params['country_id'] != None:
            country_id = params['country_id']

        if country_id:
            for item in data:
                news = db.session.query(db.NewsAppsCountriesPositions) \
                    .filter(db.NewsAppsCountriesPositions.app_id == app_id) \
                    .filter(db.NewsAppsCountriesPositions.news_id == item['item_id']) \
                    .filter(db.NewsAppsCountriesPositions.country_id == country_id).first()
                if news:
                    news.position = item['position']
                else:
                    news = db.NewsAppsCountriesPositions(app_id=app_id, news_id=item['item_id'],
                                                         country_id=country_id,
                                                         position=item['position'])
                    db.session.add(news)

        else:
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


class NewsDynamicLink(web.View):
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        try:
            if "app_id" not in params:
                return web.HTTPNoContent()
            app_id = int(params["app_id"])

            if "offer_id" not in params:
                return web.HTTPNoContent()
            offer_id = int(params["offer_id"])
        except Exception as e:
            return web.HTTPNoContent()

        app = db.session.query(db.Applications).filter(db.Applications.id == app_id).first()
        offer = db.session.query(db.News).filter(db.News.id == offer_id).first()

        app_offers = fb_client.get_all(app.fb_id)

        offer_position = 0
        for item in app_offers["news"]:
            if int(offer.id) == int(item['id']):
                break
            offer_position += 1
        offer_link = "www.{}.ru/news?id={}".format(app.fb_id, offer_position)

        rsp = {
            "link": offer_link
        }
        return web.json_response(rsp)
