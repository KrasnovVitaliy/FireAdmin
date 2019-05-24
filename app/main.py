import logging
import aiohttp_jinja2
import jinja2

from aiohttp import web
from router import routes

from config import Config
import middlewares

import base64
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

config = Config()
logging.basicConfig(filename=config.LOG_FILE, filemode='w', level=config.LOG_LEVEL, format=config.LOG_FORMAT)
logger = logging.getLogger(__name__)


def main():
    app = web.Application()
    # Creating session encrypted storage
    secret_key = base64.urlsafe_b64decode(config.COOKIE_SECRET)
    setup(app, EncryptedCookieStorage(secret_key))

    # Adding session middleware to app
    app.middlewares.append(middlewares.auth_middleware)

    # Adding jinja2 to app
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('./templates'))

    # Adding routes
    app.add_routes(routes)

    logger.info('Starting app...')
    web.run_app(app, host=config.HOST, port=config.PORT)


if __name__ == '__main__':
    main()
