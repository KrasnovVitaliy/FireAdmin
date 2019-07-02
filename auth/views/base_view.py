from aiohttp import web
from aiohttp_cors import CorsViewMixin
import logging
import json
import db
import datetime
from config import Config

logger = logging.getLogger(__name__)
config = Config()


class BaseView(web.View, CorsViewMixin):
    def __init__(self, request):
        super(BaseView, self).__init__(request=request)

        self.user_data = None
        self.post_required_fields = []
        self.post_available_fields = []
        self.post_unique_fields = []
        self.db_instance = None

    def check_user_data(self):
        get_params = self.request.rel_url.query
        if 'api_key' not in get_params:
            rsp_data = {"error": "No API key specified"}
            raise web.HTTPBadRequest(text=json.dumps(rsp_data))
        logger.debug("Getting projects with params: {}".format(get_params))
        uuid = get_params['api_key']

        if uuid == config.MASTER_API_KEY:
            return

        user = db.session.query(db.Users).filter(db.Users.api_key == uuid).first()
        if not user:
            rsp_data = {"error": "User not found"}
            raise web.HTTPNotFound(text=json.dumps(rsp_data))

        admin_role = db.session.query(db.Roles).filter(db.Roles.name == 'admin').first()
        if user.role != admin_role.id:
            rsp_data = {"error": "Not permitted request"}
            raise web.HTTPForbidden(text=json.dumps(rsp_data))

        return True

    async def __process_get_id_request(self, object_id):
        filters = {
            'deleted': None,
            'id': object_id
        }
        db_object = db.session.query(self.db_instance).filter_by(**filters).first()

        return db_object

    async def __process_get_list_request(self):
        filters = {
            'deleted': None,
        }
        db_object = db.session.query(self.db_instance).filter_by(**filters).all()

        return db_object

    async def get(self):
        self.check_user_data()

        get_params = self.request.rel_url.query
        if 'id' in get_params:
            db_object = await self.__process_get_id_request(object_id=get_params['id'])
            if not db_object:
                raise web.HTTPNotFound()
            self.ret_data = db_object.to_json()

        else:
            self.ret_data = []
            db_objects = await self.__process_get_list_request()
            for db_object in db_objects:
                self.ret_data.append(db_object.to_json())

    def __check_required_post_fields(self):
        for item in self.post_required_fields:
            if item not in self.data:
                rsp_data = {
                    "error": "Field {} not specified in request data".format(item)
                }
                raise web.HTTPBadRequest(text=json.dumps(rsp_data))

            if not self.data[item]:
                rsp_data = {
                    "error": "Field {} can not be empty".format(item)
                }
                raise web.HTTPBadRequest(text=json.dumps(rsp_data))

    def __check_unique_fields(self):
        filters = {}
        for field in self.post_unique_fields:
            filters[field] = self.data[field]

        db_objects = db.session.query(self.db_instance).filter_by(**filters).count()
        if db_objects > 0:
            rsp_data = {"error": "Such object already exists"}
            raise web.HTTPBadRequest(text=json.dumps(rsp_data))

    async def post(self):
        self.check_user_data()
        self.data = await self.request.json()
        logger.debug("Received request data: {}".format(self.data))

        self.__check_required_post_fields()
        self.__check_unique_fields()

        db_object = self.db_instance()
        for field in self.post_available_fields:
            if field in self.data:
                setattr(db_object, field, self.data[field])
        db_object.creator = self.user_data['id']

        db.session.add(db_object)
        db.session.commit()

        self.ret_data = db_object.to_json()

    async def put(self):
        self.check_user_data()
        get_params = self.request.rel_url.query
        if 'id' not in get_params:
            rsp_data = {'error': 'Id must be specified in request'}
            raise web.HTTPBadRequest(text=json.dumps(rsp_data))

        self.data = await self.request.json()

        db_object = await self.__process_get_id_request(object_id=get_params['id'])
        if not db_object:
            raise web.HTTPNotFound()

        for field in self.post_available_fields:
            if field in self.data:
                setattr(db_object, field, self.data[field])

        db.session.add(db_object)
        db.session.commit()

        self.ret_data = db_object.to_json()

    async def delete(self):
        self.check_user_data()
        get_params = self.request.rel_url.query
        if 'id' not in get_params:
            rsp_data = {'error': 'Id must be specified in request'}
            raise web.HTTPBadRequest(text=json.dumps(rsp_data))

        db_object = await self.__process_get_id_request(object_id=get_params['id'])
        if not db_object:
            raise web.HTTPNotFound()

        db_object.deleted = datetime.datetime.now()
        db.session.commit()
