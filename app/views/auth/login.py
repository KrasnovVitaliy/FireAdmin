from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm

logger = logging.getLogger(__name__)
config = Config()


class LoginView(web.View):
    @aiohttp_jinja2.template('auth/login.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query

        return {
            "auth_service_address": config.AUTH_SERVICE_ADDRESS
        }
