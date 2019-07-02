from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db
import datetime

logger = logging.getLogger(__name__)
config = Config()


def get_max_position(app_id):
    result = db.session.execute(
        "SELECT max(news_apps_relations.position)from news_apps_relations inner join news on news_apps_relations.news_id==news.id where news_apps_relations.app_id={} and news.deleted is null;".format(
            int(app_id)))
    try:
        for row in result:
            return int(row[0])
    except:
        return 0
    return 0


class NewsOverviewView(web.View):
    @aiohttp_jinja2.template('news/news_overview.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        news = db.session.query(db.News).filter_by(**filters).first()
        news_data = news.to_json()
        news_data['expireDate'] = news.expireDate.strftime("%m/%d/%Y")

        filters = {
            'deleted': None,
        }
        apps = db.session.query(db.Applications).filter_by(**filters).all()
        apps_data = [obj.to_json() for obj in apps]

        filters = {
            'news_id': params['id']
        }

        news_apps = db.session.query(db.NewsAppsRelations).filter_by(**filters).all()
        news_apps_data = [obj.app_id for obj in news_apps]

        countries = db.session.query(db.Countries).all()
        countries_data = [obj.to_json() for obj in countries]

        news_countries = db.session.query(db.NewsCountriesRelations).filter_by(**filters).all()
        news_countries_data = [obj.country_id for obj in news_countries]

        news_state = None
        if 'state' in params:
            news_state = params['state']

        current_app = None
        if 'current_app' in params:
            current_app = params['current_app']
        return {
            'offers_types': avm.offers_types(),
            'news': news_data,
            'apps': apps_data,
            'news_apps': news_apps_data,
            'active_menu_item': 'newss',
            'countries': countries_data,
            'news_countries': news_countries_data,
            'offers_state': news_state,
            'current_app': current_app,
            'auth_service_address': config.AUTH_SERVICE_ADDRESS
        }

    async def post(self, *args, **kwargs):
        params = self.request.rel_url.query

        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        filters = {
            'id': params['id']
        }
        news_item = db.session.query(db.News).filter_by(**filters).first()

        for field in post_data:
            if post_data[field].lower() == 'none':
                continue

            if field == "expireDate":
                expire_date = datetime.datetime.strptime(post_data[field], "%m/%d/%Y")
                setattr(news_item, field, expire_date)

            elif field == 'isActive':
                setattr(news_item, field, 1)

            else:
                setattr(news_item, field, post_data[field])

        if 'isActive' not in post_data:
            setattr(news_item, 'isActive', 0)

        db.session.add(news_item)
        db.session.commit()

        # Update news applications relation
        filters = {
            'news_id': params['id']
        }
        news_app_relation_old = db.session.query(db.NewsAppsRelations).filter_by(**filters).all()
        news_app_relation_old_data = {}
        for item in news_app_relation_old:
            if item.position:
                news_app_relation_old_data[int(item.app_id)] = int(item.position)

        db.session.query(db.NewsAppsRelations).filter_by(news_id=news_item.id).delete()
        db.session.query(db.NewsCountriesRelations).filter_by(**filters).delete()
        for field in post_data:
            if "app_" in field:
                app_id = field.replace('app_', '')
                news_app_relation = db.NewsAppsRelations(app_id=app_id, news_id=news_item.id)
                if int(app_id) in news_app_relation_old_data:
                    news_app_relation.position = news_app_relation_old_data[int(app_id)]
                else:
                    max_position = get_max_position(app_id)
                    news_app_relation.position = max_position + 1
                db.session.add(news_app_relation)

            elif "country_" in field:
                country_id = field.replace('country_', '')
                news_country_relation = db.NewsCountriesRelations(
                    country_id=country_id, news_id=params['id'])
                db.session.add(news_country_relation)

        db.session.commit()

        news_state = None
        if 'state' in params:
            news_state = params['state']

        current_app = None
        if 'current_app' in params:
            current_app = params['current_app']

        return web.HTTPFound('/news?state={}&current_app={}'.format(news_state, current_app))
