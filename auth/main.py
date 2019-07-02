import logging
import aiohttp_jinja2
import jinja2
import aiohttp_cors

from aiohttp import web
from router import routes

from config import Config

import base64
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage


config = Config()
logging.basicConfig(filename=config.LOG_FILE, filemode='w', level=config.LOG_LEVEL, format=config.LOG_FORMAT)
logger = logging.getLogger(__name__)


def main():
    app = web.Application()
    secret_key = base64.urlsafe_b64decode(config.COOKIE_SECRET)
    setup(app, EncryptedCookieStorage(secret_key))

    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('./templates'))

    app.add_routes(routes)

    # Add CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    for route in list(app.router.routes()):
        cors.add(route, webview=True)
    # CORS added
    logger.info('Starting app...')
    web.run_app(app, host=config.HOST, port=config.PORT)


if __name__ == '__main__':
    main()
