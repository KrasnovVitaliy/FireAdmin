from aiohttp import web
from aiohttp_cors import CorsViewMixin
from aiohttp_session import get_session

from config import Config
config = Config()

class LogoutView(web.View, CorsViewMixin):
    async def get(self):
        session = await get_session(self.request)
        del session['auth']

        params = self.request.rel_url.query
        if 'redirect_url' in params:
            return web.HTTPFound(params['redirect_url'])
        return web.HTTPOk()
