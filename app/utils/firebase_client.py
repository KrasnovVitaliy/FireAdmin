import logging
from firebase import firebase
import concurrent.futures

logger = logging.getLogger(__name__)


def get_all(project_id):
    fb = firebase.FirebaseApplication('https://{}.firebaseio.com'.format(project_id), None)
    result = fb.get('/', None)
    return result


def delete(project_id, url, name):
    fb = firebase.FirebaseApplication('https://{}.firebaseio.com'.format(project_id), None)
    result = fb.delete(url, name)
    return result


def load_all_data(project_id, data):
    fb = firebase.FirebaseApplication('https://{}.firebaseio.com'.format(project_id), None)
    if get_all(project_id):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for key in get_all(project_id).keys():
                if key != "users":
                    executor.submit(fb.delete, "/", '/{}'.format(key))
                    # fb.delete("/", '/{}'.format(key))

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for key in data.keys():
            executor.submit(fb.put, '/', '/{}'.format(key), data[key])
            # result = fb.put('/', '/{}'.format(key), data[key])
    return True
