from aiohttp import web
from aiohttp_cors import CorsViewMixin
import logging

from config import Config

logger = logging.getLogger(__name__)
config = Config()


class ConfigsView(web.View, CorsViewMixin):
    async def get(self):
        return web.json_response(config.dict())
