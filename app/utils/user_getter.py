import requests
import logging
import tokens_db
import jwt
from config import Config
from aiohttp_session import get_session

logger = logging.getLogger(__name__)
config = Config()


def get_user(user_id):
    rsp = requests.get(
        "{}/users?id={}&api_key={}".format(config.AUTH_SERVICE_INTERNAL, user_id, config.AUTH_MASTER_API_KEY))
    logger.debug("Get user code: {} response: {}".format(rsp.status_code, rsp.text))
    try:
        if rsp.status_code == 200 and rsp.json():
            return rsp.json()

    except Exception as e:
        logger.error("Can not to get user. Error is: {}".format(e))
    return {
        "id": -1,
        "role": -1,
        "create_date": "",
        "update_date": "",
        "first_name": "",
        "last_name": "",
        "email": "",
        "pass_hash": "",
        "api_key": "",
        "deleted": ""
    }


def get_role(role_id):
    rsp = requests.get(
        "{}/roles?id={}&api_key={}".format(config.AUTH_SERVICE_INTERNAL, role_id, config.AUTH_MASTER_API_KEY))
    logger.debug("Get role response: {}".format(rsp.text))
    if rsp.status_code == 200:
        return rsp.json()
    return {}


async def get_session_user(request):
    session = await get_session(request)
    logger.debug("Received session: {}".format(session))

    logger.debug("Decode auth section")
    data = tokens_db.decode_token(session['auth'])
    logger.debug("Decoded auth section data: {}".format(data))

    return get_user(user_id=data['id'])


async def get_session_user_permissions(request):
    user = await get_session_user(request)
    logger.debug("Session user: {}".format(user))
    if user['id'] != -1:
        role = get_role(user['role'])
        logger.debug("User role: {}".format(role))
        return {
            'apps_permission': role['apps_permission'],
            'offers_permission': role['offers_permission'],
            'offers_type_permission': role['offers_type_permission'],
            'news_permission': role['news_permission'],
            'countries_permission': role['countries_permission'],
            'users_permission': role['users_permission'],
            'journal_permission': role['journal_permission'],
        }
    return {
        'apps_permission': 0,
        'offers_permission': 0,
        'offers_type_permission': 0,
        'news_permission': 0,
        'countries_permission': 0,
        'users_permission': 0,
        'journal_permission': 0,
    }
