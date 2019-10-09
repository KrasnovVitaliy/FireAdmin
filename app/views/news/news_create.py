from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db
import datetime
from utils.check_permissions import is_permitted
import views.journal as journal

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


def get_max_country_news_position(app_id, country_id):
    result = db.session.execute(
        "SELECT max(position) from news_apps_countries_positions where app_id={} and country_id={};".format(
            int(app_id), int(country_id)
        ))
    try:
        for row in result:
            return int(row[0])
    except:
        return 0
    return 0


class NewsCreateView(web.View):
    @aiohttp_jinja2.template('news/news_create.html')
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['news_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query
        offer_data = {}

        filters = {
            'deleted': None,
        }
        apps = db.session.query(db.Applications).filter_by(**filters).all()
        apps_data = [obj.to_json() for obj in apps]

        countries = db.session.query(db.Countries).all()
        countries_data = [obj.to_json() for obj in countries]
        return {
            'apps': apps_data,
            "permissions": user_permissions,
            'offers_types': avm.offers_types(),
            'offer': offer_data,
            'countries': countries_data,
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL
        }

    async def post(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['news_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query

        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        news_item = db.News()

        app_ids = []
        country_ids = []

        for field in post_data:
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
        db.session.query(db.NewsAppsRelations).filter_by(news_id=news_item.id).delete()
        for field in post_data:
            if "app_" in field:
                app_id = field.replace('app_', '')
                max_position = get_max_position(app_id)
                news_app_relation = db.NewsAppsRelations(app_id=app_id, news_id=news_item.id, position=max_position + 1)
                db.session.add(news_app_relation)
                app_ids.append(app_id)
            elif "country_" in field:
                country_id = field.replace('country_', '')
                news_country_relation = db.NewsCountriesRelations(
                    country_id=country_id, news_id=news_item.id)
                db.session.add(news_country_relation)
                country_ids.append(country_id)

        db.session.commit()

        for app_id in app_ids:
            for country_id in country_ids:
                news_position = db.session.query(db.NewsAppsCountriesPositions) \
                    .filter(db.NewsAppsCountriesPositions.news_id == news_item.id) \
                    .filter(db.NewsAppsCountriesPositions.country_id == country_id) \
                    .filter(db.NewsAppsCountriesPositions.app_id == app_id).first()

                if not news_position:
                    position = get_max_country_news_position(app_id=app_id,
                                                             country_id=country_id)
                    news_position = db.NewsAppsCountriesPositions(app_id=app_id, news_id=news_item.id,
                                                                  country_id=country_id,
                                                                  position=position + 1)
                    db.session.add(news_position)

        db.session.commit()

        await journal.add_action(request=self.request, object_type=journal.CREATE_ACTION,
                                 action=journal.DELETE_ACTION,
                                 description=str(news_item.to_json()))


        return web.HTTPFound('/news')
