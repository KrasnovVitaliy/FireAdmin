from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db

logger = logging.getLogger(__name__)
config = Config()


class NewsView(web.View):
    @aiohttp_jinja2.template('news.html')
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

        news = db.session.query(db.News).filter_by(**filters).all()
        news_data = [obj.to_json() for obj in news]

        return {
            'news': news_data,
            'offers_types': avm.offers_types(),
            'news_state': news_state,
            'active_menu_item': 'news'
        }
