from aiohttp import web
from config import Config
import logging
import json
import db


import utils.firebase_client as fb_client
from utils.data_to_json import gen_app_json

logger = logging.getLogger(__name__)
config = Config()


class AppsFBDBGetView(web.View):
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        app = db.session.query(db.Applications).filter_by(id=params['id']).first()

        data = fb_client.get_all(app.fb_id)
        if not data:
            return web.HTTPError(body=data)

        return web.HTTPOk(body=json.dumps(data, ensure_ascii=False), headers={
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename=fb_{}.json'.format(app.name),
            'Content-Transfer-Encoding': 'binary',
        })


class AppsFBDBLoadView(web.View):
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        app = db.session.query(db.Applications).filter_by(id=params['id']).first()
        data = gen_app_json(app)

        data = fb_client.load_all_data(app.fb_id, data)
        if not data:
            return web.HTTPError(body=data)

        return web.HTTPFound('/applications')
