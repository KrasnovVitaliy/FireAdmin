import logging
from config_base import ConfigBase
import sys
import os


class Config(ConfigBase):
    VERSION = "1.0.0"
    IS_DEBUG = False
    IS_LOCAL = False

    PORT = 8070
    HOST = "0.0.0.0"

    if IS_LOCAL:
        DB_URI = 'sqlite:///./fireadmin2.db'
    else:
        DB_URI = 'sqlite:////root/fireadmin2.db'
    # DB_URI = "postgresql://fireadmin:thoRIUM87@@51.159.27.4:58938/fireadmin"

    # Logging
    LOG_FORMAT = '%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s'
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = None

    AUTH_SERVICE_INTERNAL = "http://127.0.0.1:8071"
    if IS_LOCAL:
        AUTH_SERVICE_EXTERNAL = "http://127.0.0.1:8071"
    else:
        AUTH_SERVICE_EXTERNAL = "http://51.158.176.243:8071"

    TOKENS_SECRET = "fdad66f77d284d18bf9381eb406f334f"  # uuid.uuid4().hex
    COOKIE_SECRET = "NmIzYjI5N2I2OWJjNGM0Nzk3MzY1ZTdlMTM0NWRkNTY="  # base64.b64encode(uuid.uuid4().hex.encode())  #
    AUTH_MASTER_API_KEY = "6b3b297b69bc4c4797365e7e1345dd56"

    NON_LOGIN_URLS = [
        'login',
        'logout',
        'signup',
        'static'
    ]

    FILE_UPLOAD_PATH = './'
    os.chdir(os.path.dirname(__file__))
    PROJECT_DIR = os.getcwd()
    sys.path.append(PROJECT_DIR)

    # AUTH_SERVICE_ADDRESS = "http://51.158.176.243:8081"
