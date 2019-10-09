from aiohttp import web
import logging
from config import Config
import json
import db
from utils.data_to_json import gen_app_json
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()


class AppsDBJsonView(web.View):
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])
        params = self.request.rel_url.query

        app = db.session.query(db.Applications).filter_by(id=params['id']).first()
        ret_data = gen_app_json(app)

        return web.HTTPOk(body=json.dumps(ret_data, ensure_ascii=False), headers={
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Disposition': 'attachment; filename={}.json'.format(app.name),
            'Content-Transfer-Encoding': 'utf-8',
        })
