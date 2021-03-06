from aiohttp import web
import datetime
import logging
from config import Config
import views.all_view_methods as avm
import db
import utils.firebase_client as fb_client
from utils.check_permissions import is_permitted
import views.journal as journal

logger = logging.getLogger(__name__)
config = Config()


class NewsActionsView(web.View):
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['news_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        news = db.session.query(db.News).filter_by(**filters).first()
        if params['action'] == 'run':
            news.isActive = 1
            await journal.add_action(request=self.request, object_type=journal.NEWS_OBJECT,
                                     action=journal.START_ACTION,
                                     description=str(news.to_json()))
        elif params['action'] == 'stop':
            news.isActive = 0
            await journal.add_action(request=self.request, object_type=journal.NEWS_OBJECT,
                                     action=journal.STOP_ACTION,
                                     description=str(news.to_json()))
        elif params['action'] == 'delete':
            news.deleted = datetime.datetime.now()
            await journal.add_action(request=self.request, object_type=journal.NEWS_OBJECT,
                                     action=journal.DELETE_ACTION,
                                     description=str(news.to_json()))
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        return web.HTTPFound('news')


class NewsUpdateOrder(web.View):
    async def post(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['news_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

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

                await journal.add_action(request=self.request, object_type=journal.NEWS_OBJECT,
                                         action=journal.REORDER_ACTION,
                                         description=str(news.to_json()))

        else:
            # for item in data:
            #     logger.debug("Post data: {}".format(item))
            #     news = db.session.query(db.NewsAppsRelations).filter_by(app_id=app_id, news_id=item['item_id']).first()
            #     news.position = item['position']

            for item in data:
                news = db.session.query(db.NewsAppsCountriesPositions) \
                    .filter(db.NewsAppsCountriesPositions.app_id == app_id) \
                    .filter(db.NewsAppsCountriesPositions.news_id == item['item_id']) \
                    .filter(db.NewsAppsCountriesPositions.country_id == -1).first()
                if news:
                    news.position = item['position']
                else:
                    news = db.NewsAppsCountriesPositions(app_id=app_id, news_id=item['item_id'],
                                                         country_id=-1,
                                                         position=item['position'])
                    db.session.add(news)

                await journal.add_action(request=self.request, object_type=journal.NEWS_OBJECT,
                                         action=journal.REORDER_ACTION,
                                         description=str(news.to_json()))

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return web.HTTPOk()


class NewsUpdateComment(web.View):
    async def post(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['news_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        data = await self.request.json()

        logger.debug("Post data: {}".format(data))
        offer = db.session.query(db.News).filter_by(id=data['item_id']).first()
        offer.comment = data['comment']

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return web.HTTPOk()


class NewsDynamicLink(web.View):
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['news_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

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

        country_code = None
        if "country_code" in params:
            country_code = params["country_code"]

        app = db.session.query(db.Applications).filter(db.Applications.id == app_id).first()
        offer = db.session.query(db.News).filter(db.News.id == offer_id).first()

        app_offers = fb_client.get_all(app)

        offer_position = 0
        for item in app_offers["news"]:
            if int(offer.id) == int(item['id']):
                break
            offer_position += 1
        offer_link = "www.{}.ru/news?id={}".format(app, offer_position)

        country_offer_link = "Страна не задана"
        if country_code:
            country_offer_link = "http://www.{}.ru/offer_item/{}/news/{}".format(
                app, country_code, offer_position)

        rsp = {
            "link": offer_link,
            "country_link": country_offer_link
        }

        return web.json_response(rsp)
