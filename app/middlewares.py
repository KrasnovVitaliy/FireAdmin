from aiohttp import web
from config import Config
# from aiohttp_session import get_session
# import tokens_db
import logging
# import jwt

logger = logging.getLogger(__name__)
config = Config()

@web.middleware
async def auth_middleware(request, handler):
    # try:
    #     splitted_path = request.url.path.split("/")
    #     if splitted_path[1] in config.NON_LOGIN_URLS:
    #         response = await handler(request)
    #         return response
    #
    #     session = await get_session(request)
    #     logger.debug("Received session: {}".format(session))
    #
    #     logger.debug("Is auth section in cookies session")
    #     if 'auth' not in session:
    #         logger.debug("No auth sections in cookies")
    #         return web.HTTPFound('/login')
    #
    #     logger.debug("Decode auth section")
    #     data = tokens_db.decode_token(session['auth'])
    #     logger.debug("Decoded auth section data: {}".format(data))
    #
    #
    # except web.HTTPException as ex:
    #     logger.warning("Http error")
    #     if ex.status != 404:
    #         raise
    #
    # except jwt.DecodeError:
    #     logger.warning("Incorrect JWT token")
    #     return web.HTTPFound('/login')

    response = await handler(request)
    return response
