from aiohttp import web
import aiohttp_jinja2
import logging

from config import Config

logger = logging.getLogger(__name__)
config = Config()


class ConfigsView(web.View):
    async def get(self):
        return web.json_response(config.dict())