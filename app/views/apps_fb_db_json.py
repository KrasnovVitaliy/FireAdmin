from aiohttp import web
import logging
from config import Config
import json
import db
from utils.trim_fields import trim_fields
import utils.firebase_client as fb_client

logger = logging.getLogger(__name__)
config = Config()


class AppsFBDBGetView(web.View):
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'app_id': params['id']
        }

        app = db.session.query(db.Applications).filter_by(id=params['id']).first()

        stuts_code, rsp_data = fb_client.get_all(app.fb_id)
        if stuts_code != 200:
            return web.HTTPError(body=rsp_data)

        return web.HTTPOk(body=json.dumps(rsp_data), headers={
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename=fb_{}.json'.format(app.name),
            'Content-Transfer-Encoding': 'binary',
        })


class AppsFBDBLoadView(web.View):
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        filters = {
            'app_id': params['id']
        }

        app = db.session.query(db.Applications).filter_by(id=params['id']).first()
        results = db.session.query(db.OffersAppsRelations, db.Offers).filter_by(**filters).filter(
            db.OffersAppsRelations.offer_id == db.Offers.id).all()

        data = {}
        for result in results:
            offer_data = trim_fields(result[1].to_json())

            offer_type = db.session.query(db.OffersTypes).filter_by(id=result[1].offer_type).first()

            if offer_type.name not in data:
                data[offer_type.name] = []
            data[offer_type.name].append(offer_data)

        stuts_code, rsp_data = fb_client.load_all_data(app.fb_id, data)
        if stuts_code != 200:
            return web.HTTPError(body=rsp_data)

        return web.HTTPFound('/applications')
