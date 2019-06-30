import requests
import logging
import json
import datetime
import os
from firebase import firebase

logger = logging.getLogger(__name__)

url = "http://127.0.0.1:8080"
current_date = datetime.datetime.now().strftime('%d_%m_%y_%H')
backup_path = "/root/firebase_backup/{}".format(current_date)

os.makedirs(backup_path)


def get_all(project_id):
    fb = firebase.FirebaseApplication('https://{}.firebaseio.com'.format(project_id), None)
    result = fb.get('/', None)
    return json.dumps(result, ensure_ascii=False)


apps = requests.get('{}/applications_json'.format(url))

for app in apps.json():
    with open("{}/{}.json".format(backup_path, app['fb_id']), 'w') as out_file:
        out_file.write(get_all(app['fb_id']))
