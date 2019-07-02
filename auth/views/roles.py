from aiohttp import web

import db
from views.base_view import BaseView


class RolesView(BaseView):
    def __init__(self, request):
        """
            description: API roles endpoint
        """
        super(RolesView, self).__init__(request=request)
        self.db_instance = db.Roles
        self.post_required_fields = ['name']
        self.post_available_fields = ['name']
        self.post_unique_fields = ['name']

    async def get(self):
        """
            arg: id:int:role id:required

            ret: id:int:role id
            ret: create_date:datetime:role creation datetime
            ret: update_date:datetime:role update datetime
            ret: name:str:role name
            ret: deleted:datetime:project deleted datetime
        """
        await super(RolesView, self).get()
        return web.json_response(self.ret_data)

    async def post(self):
        """
            body: name:str:role name:required

            ret: id:int:role id
            ret: create_date:datetime:role creation datetime
            ret: update_date:datetime:role update datetime
            ret: name:str:role name
            ret: deleted:datetime:project deleted datetime
        """
        await super(RolesView, self).post()
        return web.json_response(self.ret_data, status=201)

    async def put(self):
        """
            arg: id:int:role id:required

            body: name:str:role name

            ret: id:int:role id
            ret: create_date:datetime:role creation datetime
            ret: update_date:datetime:role update datetime
            ret: name:str:role name
            ret: deleted:datetime:project deleted datetime
        """

        await super(RolesView, self).put()
        return web.json_response(self.ret_data, status=200)

    async def delete(self):
        """
            arg: id:int:role id:required
        """
        await super(RolesView, self).delete()
        return web.json_response({}, status=200)
