from aiohttp import web
import logging
from config import Config
import json
import db
from utils.data_to_json import gen_app_json
from utils.check_permissions import is_permitted
from utils.ftp_client import upload_to_ftp
import datetime

logger = logging.getLogger(__name__)
config = Config()


class AppsFTPUpdate(web.View):
    async def get(self, *args, **kwargs):
        logger.debug("Update FTP json")
        user_permissions = is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])
        params = self.request.rel_url.query

        app = db.session.query(db.Applications).filter_by(id=params['id']).first()
        ret_data = gen_app_json(app)

        with open("./db.json", "w") as out:
            out.write(json.dumps(ret_data, ensure_ascii=False))

        logger.debug("Upload file to FTP: {} username {} password {}".format(
            app.ftp_path, app.ftp_username, app.ftp_password))

        logger.info("Upload db.json to ftp")
        upload_to_ftp(ftp_host=app.ftp_path, ftp_path="/", path_to_local_file="./db.json",
                      ftp_username=app.ftp_username, ftp_password=app.ftp_password)

        logger.debug("Create date.json file")
        with open("date.json", "w") as out:
            out.write(datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))

        logger.info("Upload date.json to ftp")
        upload_to_ftp(ftp_host=app.ftp_path, ftp_path="/", path_to_local_file="./date.json",
                      ftp_username=app.ftp_username, ftp_password=app.ftp_password)

        return web.HTTPOk()
