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
    IS_DEBUG = False
    IS_LOCAL = False

    PORT = 8071
    HOST = "0.0.0.0"

    if IS_LOCAL:
        DB_URI = 'sqlite:///./fireadmin_auth2.db'
    else:
        DB_URI = 'sqlite:////root/fireadmin_auth2.db'

    # Logging
    LOG_FORMAT = '%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s'
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = None

    TOKENS_SECRET = "fdad66f77d284d18bf9381eb406f334f"  # uuid.uuid4().hex
    COOKIE_SECRET = "NmIzYjI5N2I2OWJjNGM0Nzk3MzY1ZTdlMTM0NWRkNTY="  # base64.b64encode(uuid.uuid4().hex.encode())  #
    MASTER_API_KEY = "6b3b297b69bc4c4797365e7e1345dd56"

    if IS_LOCAL:
        MAIN_SERVICE_EXTERNAL = 'http://127.0.0.1:8070'
    else:
        MAIN_SERVICE_EXTERNAL = 'http://151.236.217.166:8070'

    os.chdir(os.path.dirname(__file__))
    PROJECT_DIR = os.getcwd()
    sys.path.append(PROJECT_DIR)
