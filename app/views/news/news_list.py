from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db
from sqlalchemy import asc

logger = logging.getLogger(__name__)
config = Config()


class NewsView(web.View):
    @aiohttp_jinja2.template('news/news.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'deleted': None,
        }
        if 'state' in params:
            news_state = params['state'].lower()
            if news_state == 'active':
                filters['isActive'] = 1
            elif news_state == 'inactive':
                filters['isActive'] = 0
        else:
            news_state = 'all'

        news = db.session.query(db.News).filter_by(**filters).order_by(asc(db.News.position)).all()
        news_data = [obj.to_json() for obj in news]

        apps = db.session.query(db.Applications).all()
        app_data = {}
        for app in apps:
            app_data[app.id] = app.to_json()

        for news_item in news_data:
            if 'related_apps' not in news_item:
                news_item['related_apps'] = []

            news_apps = db.session.query(db.NewsAppsRelations).filter_by(news_id=news_item['id']).all()
            for news_app in news_apps:
                news_item['related_apps'].append(app_data[news_app.app_id])
        return {
            'news': news_data,
            'offers_types': avm.offers_types(),
            'news_state': news_state,
            'active_menu_item': 'news'
        }