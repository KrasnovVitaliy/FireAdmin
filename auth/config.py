import logging
from config_base import ConfigBase
import os
import sys
import uuid
import base64


class SingletonDecorator:
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance == None:
            self.instance = self.klass(*args, **kwds)
        return self.instance


@SingletonDecorator
class Config(ConfigBase):
    VERSION = "1.0.0"
    IS_DEBUG = True

    PORT = 8081
    HOST = "0.0.0.0"

    # DB_URI = 'sqlite:////root/fireadmin_auth.db'
    DB_URI = 'sqlite:///./auth.db'

    # Logging
    LOG_FORMAT = '%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s'
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = None

    TOKENS_SECRET = "nzIxhdYtE4UUDITCHst9bhvSJsuhPMbYNostg28oM"  # uuid.uuid4().hex
    COOKIE_SECRET = "kioQTiAtFMoncsZOYRnj5IvagCndNV2e9LFy1RNEMOU="  # base64.b64encode(uuid.uuid4().hex.encode())  #
    MASTER_API_KEY = "a4e2cbe005ad54e2d8d101fcd2618f87"

    MAIN_SERVICE_INTERNAL = 'http://127.0.0.1:8080'
    MAIN_SERVICE_EXTERNAL = 'http://51.158.176.243:8080'

    os.chdir(os.path.dirname(__file__))
    PROJECT_DIR = os.getcwd()
    sys.path.append(PROJECT_DIR)
