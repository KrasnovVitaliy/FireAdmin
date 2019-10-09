from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db
from sqlalchemy import asc
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()


class NewsView(web.View):
    def filter_news_by_countries(self, news, country_id):
        news_list = []
        for news_item in news:
            result = db.session.query(db.NewsCountriesRelations) \
                .filter(db.NewsCountriesRelations.news_id == news_item.id) \
                .filter(db.NewsCountriesRelations.country_id == country_id).first()

            if result:
                news_list.append(news_item)

        return news_list

    def get_news_country_position(self, news_id, country_id, app_id):
        news_item = db.session.query(db.NewsAppsCountriesPositions) \
            .filter(db.NewsAppsCountriesPositions.news_id == news_id) \
            .filter(db.NewsAppsCountriesPositions.country_id == country_id) \
            .filter(db.NewsAppsCountriesPositions.app_id == app_id).first()

        if news_item:
            return news_item.position
        return 0

    @aiohttp_jinja2.template('news/news.html')
    async def get(self, *args, **kwargs):
        user_permissions = await is_permitted(self.request, ['news_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

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

        try:
            current_app = int(params['current_app'])
        except Exception as e:
            current_app = None

        try:
            current_country = int(params['current_country'])
        except Exception as e:
            current_country = None

        if current_app:
            results = db.session.query(db.NewsAppsRelations, db.News) \
                .filter(db.NewsAppsRelations.app_id == current_app) \
                .filter(db.NewsAppsRelations.news_id == db.News.id) \
                .filter(db.News.deleted == None)
            if 'isActive' in filters:
                results = results.filter(db.News.isActive == filters['isActive'])

            results = results.order_by(asc(db.NewsAppsRelations.position)).all()

            # Building offers list from results
            news = [result[1] for result in results]

        else:
            news = db.session.query(db.News).filter_by(**filters).order_by(asc(db.News.position)).all()

        if current_country:
            news = self.filter_news_by_countries(news, current_country)

        news_data = [obj.to_json() for obj in news]

        apps = db.session.query(db.Applications).all()
        app_data = {}
        for app in apps:
            app_data[app.id] = app.to_json()

        # for news_item in news_data:
        #     if 'related_apps' not in news_item:
        #         news_item['related_apps'] = []
        #
        #     news_apps = db.session.query(db.NewsAppsRelations).filter_by(news_id=news_item['id']).all()
        #     for news_app in news_apps:
        #         news_item['related_apps'].append(app_data[news_app.app_id])

        filters = {
            'deleted': None,
        }
        apps = db.session.query(db.Applications).filter_by(**filters).all()
        apps_data = [obj.to_json() for obj in apps]

        for news in news_data:
            if 'related_apps' not in news:
                news['related_apps'] = []
            if 'app_position' not in news:
                news['app_position'] = 0

            news_apps = db.session.query(db.NewsAppsRelations).filter_by(news_id=news['id']).all()
            for news_app in news_apps:
                news['related_apps'].append(app_data[news_app.app_id])
                # news['app_position'][news_app.app_id] = news_app.position

                if current_app:
                    if current_country:
                        news['app_position'] = self.get_news_country_position(
                            news_id=news['id'], country_id=current_country, app_id=current_app)
                    else:
                        news['app_position'] = self.get_news_country_position(
                            news_id=news['id'], country_id=-1, app_id=current_app)

                        if not news['app_position']:
                            news['app_position'] = 0
                else:
                    news['app_position'] = 0

        if current_app:
            for app in apps_data:
                if app['id'] == int(current_app):
                    current_app = app
                    break

        news_data = sorted(news_data, key=lambda k: k['app_position'])

        countries = db.session.query(db.Countries).all()
        countries_data = [obj.to_json() for obj in countries]

        if current_country:
            for country in countries_data:
                if country['id'] == int(current_country):
                    current_country = country
                    break
        return {
            'news': news_data,
            "permissions": user_permissions,
            'offers_types': avm.offers_types(),
            'news_state': news_state,
            'active_menu_item': 'news',
            'apps': apps_data,
            'current_app': current_app,
            'countries': countries_data,
            'current_country': current_country,
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL
        }
