from aiohttp import web
import datetime
import time
import db
from views.base_view import BaseView
import logging
import hashlib

import tokens_db
from config import Config

logger = logging.getLogger(__name__)
config = Config()


class UsersView(BaseView):
    def create_api_key(self):
        m = hashlib.md5()
        m.update(str(time.time()).encode('utf-8'))
        return m.hexdigest()

    def __init__(self, request):
        """
            description: API roles endpoint
        """
        super(UsersView, self).__init__(request=request)
        self.db_instance = db.Users
        self.post_required_fields = ['email', 'password']
        self.post_available_fields = ['email', 'password', 'first_name', 'last_name', 'api_key']
        self.post_unique_fields = ['email']

    async def get(self):
        """
            arg: id:int:role id:required

            ret: id:int:role id
            ret: create_date:datetime:role creation datetime
            ret: update_date:datetime:role update datetime
            ret: name:str:role name
            ret: deleted:datetime:project deleted datetime
        """
        await super(UsersView, self).get()
        return web.json_response(self.ret_data)

    async def post(self):
        self.check_user_data()

        data = await self.request.json()
        logger.debug("Received login request data: {}".format(data))
        logger.debug("Is email and password fields present")
        if "email" not in data or "password" not in data:
            return web.json_response({"error": "No email or password field in request body"}, status=400)

        if data['password'] == '' or data['email'] == '':
            return web.json_response({"error": "Email, password and password repeat can not be empty"}, status=400)

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

        data = users.to_json()
        del data['pass_hash']

        return web.json_response(data)

    async def put(self):
        self.check_user_data()

        data = await self.request.json()
        params = self.request.rel_url.query
        logger.debug("Updating new user with data: {} and params: {}".format(data, params))

        user = db.session.query(db.Users).filter(db.Users.email == data['email']).first()
        if user:
            return web.json_response({"error": "Email already in used"}, status=400)

        user = db.session.query(db.Users).filter(db.Users.id == params['id']).first()
        if not user:
            return web.json_response({"error": "User not found"}, status=404)

        if 'password' in data:
            if data['password']:
                logger.debug("Hashing password")
                hashed_password = tokens_db.get_hashed_password(data['password'])
                user.pass_hash = hashed_password

        for key in ['first_name', 'last_name', 'email']:
            if key in data:
                setattr(user, key, data[key])

        db.session.commit()

        data = user.to_json()
        if 'pass_hash' in data:
            del data['pass_hash']

        return web.json_response(data)

    async def delete(self):
        self.check_user_data()

        params = self.request.rel_url.query
        logger.debug("Delete user with params: {}".format(params))
        user = db.session.query(db.Users).filter(db.Users.id == params['id']).first()
        if not user:
            return web.json_response({"error": "User not found"}, status=404)

        user.deleted = datetime.datetime.now()
        db.session.commit()
        logger.debug("User removed")
        return web.json_response({})
