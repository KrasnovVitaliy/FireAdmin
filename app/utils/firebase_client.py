import logging
from firebase import firebase
import concurrent.futures

logger = logging.getLogger(__name__)


def get_all(app):
    authentication = None
    if app.fb_key:
        authentication = firebase.FirebaseAuthentication(app.fb_key, 'admin@gmail.com', True, True)

    fb = firebase.FirebaseApplication('https://{}.firebaseio.com'.format(app.fb_id), authentication)
    result = fb.get('/', None)
    return result


def delete(app, url, name):
    authentication = None
    if app.fb_key:
        authentication = firebase.FirebaseAuthentication(app.fb_key, 'admin@gmail.com', True, True)
    fb = firebase.FirebaseApplication('https://{}.firebaseio.com'.format(app.fb_id), authentication)
    result = fb.delete(url, name)
    return result


def load_all_data(app, data):
    authentication = None
    if app.fb_key:
        authentication = firebase.FirebaseAuthentication(app.fb_key, 'admin@gmail.com', True, True)

    fb = firebase.FirebaseApplication('https://{}.firebaseio.com'.format(app.fb_id), authentication)
    if get_all(app):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for key in get_all(app).keys():
                if key != "users":
                    executor.submit(fb.delete, "/", '/{}'.format(key))
                    # fb.delete("/", '/{}'.format(key))

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for key in data.keys():
            executor.submit(fb.put, '/', '/{}'.format(key), data[key])
            # result = fb.put('/', '/{}'.format(key), data[key])
    return True
