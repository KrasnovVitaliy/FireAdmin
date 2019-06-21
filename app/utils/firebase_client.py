import logging
from firebase import firebase

logger = logging.getLogger(__name__)


def get_all(project_id):
    fb = firebase.FirebaseApplication('https://{}.firebaseio.com'.format(project_id), None)
    result = fb.get('/', None)
    return result


def load_all_data(project_id, data):
    fb = firebase.FirebaseApplication('https://{}.firebaseio.com'.format(project_id), None)
    result = fb.put('/', '/', data)
    return result
