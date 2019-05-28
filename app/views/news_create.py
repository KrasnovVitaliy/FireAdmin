from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db
import datetime

logger = logging.getLogger(__name__)
config = Config()


class NewsCreateView(web.View):
    @aiohttp_jinja2.template('news_create.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query
        offer_data = {}

        apps = db.session.query(db.Applications).all()
        apps_data = [obj.to_json() for obj in apps]

        return {
            'apps': apps_data,
            'offers_types': avm.offers_types(),
            'offer': offer_data
        }

    async def post(self, *args, **kwargs):
        params = self.request.rel_url.query

        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        news_item = db.News()
        if 'isActive' not in post_data:
            setattr(news_item, 'isActive', 0)

        for field in post_data:
            if field == "expireDate":
                expire_date = datetime.datetime.strptime(post_data[field], "%m/%d/%Y")
                setattr(news_item, field, expire_date)
            else:
                setattr(news_item, field, post_data[field])

        db.session.add(news_item)
        db.session.commit()

        # Update news applications relation
        db.session.query(db.NewsAppsRelations).filter_by(news_id=news_item.id).delete()
        for field in post_data:
            if "app_" in field:
                news_app_relation = db.NewsAppsRelations(app_id=field.replace('app_', ''), news_id=news_item.id)
                db.session.add(news_app_relation)

        db.session.commit()

        return web.HTTPFound('/news')

