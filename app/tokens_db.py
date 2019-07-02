import jwt
import logging
import bcrypt

from config import Config

logger = logging.getLogger(__name__)
config = Config()


def encode_token(data):
    encoded_jwt = jwt.encode(data, config.TOKENS_SECRET, algorithm='HS256')
    return encoded_jwt


def decode_token(encoded_data):
    data = jwt.decode(encoded_data, config.TOKENS_SECRET, algorithms=['HS256'])
    return data


def get_hashed_password(password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_password(password, hashed_password):
    # Check hased password. Useing bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(password, hashed_password)
