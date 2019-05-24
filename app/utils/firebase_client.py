import requests
import logging
import json

logger = logging.getLogger(__name__)


def get_all(project_id):
    rsp = requests.get('https://{}.firebaseio.com/.json'.format(project_id))
    if rsp.status_code != 200:
        logger.error("Can not get data from firebase for project: {}. Response: {}".format(
            project_id, rsp.text))
        return None

    return json.loads(rsp.text)


def get_path(project_id, path):
    rsp = requests.get('https://{}.firebaseio.com{}.json'.format(project_id, path))
    if rsp.status_code != 200:
        logger.error("Can not get data from firebase for project: {}. Response: {}".format(
            project_id, rsp.text))
        return None

    return json.loads(rsp.text)
