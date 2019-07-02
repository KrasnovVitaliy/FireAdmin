from aiohttp import web
from aiohttp_cors import CorsViewMixin
import logging
import time

import tokens_db
from config import Config
import db
import hashlib

logger = logging.getLogger(__name__)
config = Config()


class FormUsersView(web.View, CorsViewMixin):
    def create_api_key(self):
        m = hashlib.md5()
        m.update(str(time.time()).encode('utf-8'))
        return m.hexdigest()

    async def post(self):
        data = await self.request.post()
        logger.debug("Received login request data: {}".format(data))
        logger.debug("Is email and password fields present")
        if "email" not in data or "password" not in data:
            return web.json_response({"error": "No email or password field in request body"}, status=400)

        if data['password'] == '' or data['password_repeat'] == '' or data['email'] == '':
            return web.json_response({"error": "Email, password and password repeat can not be empty"}, status=400)

        if data['password'] != data['password_repeat']:
            return web.json_response({"error": "Password and password repeat not equal"}, status=400)

        user = db.session.query(db.Users).filter(db.Users.email == data['email']).first()
        if user:
            return web.json_response({"error": "Email already in used"}, status=400)

        logger.debug("Hashing password")
        hashed_password = tokens_db.get_hashed_password(data['password'])

        user_role = db.session.query(db.Roles).filter(db.Roles.name == 'user').first()
        users = db.Users()
        for key in ['first_name', 'last_name', 'email']:
            if key in data:
                print("Param: {}: {}".format(key, data[key]))
                setattr(users, key, data[key])
        users.pass_hash = hashed_password
        users.api_key = self.create_api_key()
        users.role = user_role.id
        db.session.add(users)
        db.session.commit()
        return web.HTTPFound("{}/login".format(config.MAIN_SERVICE_EXTERNAL))
