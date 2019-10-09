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
    try:
        return rsp.json()
    except Exception as e:
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
    return rsp.json()


async def get_session_user(request):
    session = await get_session(request)
    logger.debug("Received session: {}".format(session))

    logger.debug("Decode auth section")
    data = tokens_db.decode_token(session['auth'])
    logger.debug("Decoded auth section data: {}".format(data))

    return get_user(user_id=data['id'])


async def get_session_user_permissions(request):
    user = await get_session_user(request)
    role = get_role(user['role'])
    print(role)
    return {
        'apps_permission': role['apps_permission'],
        'offers_permission': role['offers_permission'],
        'offers_type_permission': role['offers_type_permission'],
        'news_permission': role['news_permission'],
        'countries_permission': role['countries_permission'],
        'users_permission': role['users_permission'],
        'journal_permission': role['journal_permission'],
    }
