from aiohttp import web
import logging
from config import Config
import json
import db
from utils.trim_fields import trim_fields

logger = logging.getLogger(__name__)
config = Config()


class AppsDBJsonView(web.View):
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'app_id': params['id']
        }

        app = db.session.query(db.Applications).filter_by(id=params['id']).first()
        results = db.session.query(db.OffersAppsRelations, db.Offers).filter_by(**filters).filter(
            db.OffersAppsRelations.offer_id == db.Offers.id).all()

        ret_data = {}
        for result in results:
            offer_data = trim_fields(result[1].to_json())

            offer_type = db.session.query(db.OffersTypes).filter_by(id=result[1].offer_type).first()

            if offer_type.name not in ret_data:
                ret_data[offer_type.name] = []
            ret_data[offer_type.name].append(offer_data)

        return web.HTTPOk(body=json.dumps(ret_data), headers={
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename={}.json'.format(app.name),
            'Content-Transfer-Encoding': 'binary',
        })
