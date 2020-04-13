from aiohttp import web
from config import Config
import logging
import json
import db
from utils.check_permissions import is_permitted

import utils.firebase_client as fb_client
from utils.data_to_json import gen_app_json

logger = logging.getLogger(__name__)
config = Config()


class AppsFBDBGetView(web.View):
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query

        app = db.session.query(db.Applications).filter_by(id=params['id']).first()

        data = fb_client.get_all(app)
        if not data:
            return web.HTTPError(body=data)

        return web.HTTPOk(body=json.dumps(data, ensure_ascii=False), headers={
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename=fb_{}.json'.format(app.name),
            'Content-Transfer-Encoding': 'binary',
        })


class AppsFBDBLoadView(web.View):
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query

        app = db.session.query(db.Applications).filter_by(id=params['id']).first()
        data = gen_app_json(app)

        data = fb_client.load_all_data(app, data)
        if not data:
            return web.HTTPError(body=data)

        if 'redirect_uri' in params:
            logger.debug("Redirection uri: {}".format(params['redirect_uri']))
            return web.HTTPFound(params['redirect_uri'])
        else:
            return web.HTTPFound('/applications')
