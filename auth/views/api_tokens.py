from aiohttp import web
from aiohttp_cors import CorsViewMixin
import logging
from config import Config
import db

logger = logging.getLogger(__name__)
config = Config()


class ApiTokenView(web.View, CorsViewMixin):
    async def get(self):
        params = self.request.rel_url.query
        logger.debug("Getting user with params: {}".format(params))

        if 'uuid' not in params:
            return web.json_response({"error": "No uuid specified"}, status=400)

        else:
            logger.debug("Getting user by uuid: {}".format(params['uuid']))
            user = db.session.query(db.Users).filter(db.Users.api_key == params['uuid']).first()

            if not user:
                return web.json_response({"error": "User not found"}, status=404)

            data = user.to_json()
            del data['pass_hash']
            del data['api_key']

            logger.debug("Found user: {}".format(data))
            return web.json_response(data)
