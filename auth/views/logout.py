from aiohttp import web
from aiohttp_cors import CorsViewMixin
from aiohttp_session import get_session

from config import Config
config = Config()

class LogoutView(web.View, CorsViewMixin):
    async def get(self):
        session = await get_session(self.request)
        del session['auth']
        return web.HTTPFound("{}/login".format(config.MAIN_SERVICE_EXTERNAL))
