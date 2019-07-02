from aiohttp import web
from aiohttp_cors import CorsViewMixin

from config import Config
import router
import logging

logger = logging.getLogger(__name__)
config = Config()


class DocsView(web.View, CorsViewMixin):
    def __init__(self, request):
        super(DocsView, self).__init__(request=request)
        self.documented_methods = ["get", "post", "put", "delete"]

    def parse_description(self, data):
        if not data:
            return data

        return data.split(":")[1].strip()

    def parse_args(self, data):
        if not data:
            return data

        ret_data = []
        for l in data.split('\n'):
            arg_desc = {}
            if "arg:" in l:
                arg = l.split(":")
                arg_desc['name'] = arg[1].strip()
                arg_desc['type'] = arg[2].strip()
                arg_desc['description'] = arg[3]

                arg_desc['required'] = False
                if len(arg) > 4:
                    if arg[4] == 'required':
                        arg_desc['required'] = True

            if arg_desc:
                ret_data.append(arg_desc)

        return ret_data

    def parse_body(self, data):
        if not data:
            return data

        ret_data = []
        for l in data.split('\n'):
            body_desc = {}
            if "body:" in l:
                body = l.split(":")
                body_desc['name'] = body[1].strip()
                body_desc['type'] = body[2].strip()
                body_desc['description'] = body[3]

                body_desc['required'] = False
                if len(body) > 4:
                    body_desc['required'] = True

            if body_desc:
                ret_data.append(body_desc)

        return ret_data

    def parse_rets(self, data):
        if not data:
            return data

        ret_data = []
        for l in data.split('\n'):
            ret_desc = {}
            if "ret:" in l:
                ret = l.split(":")
                ret_desc['name'] = ret[1].strip()
                ret_desc['type'] = ret[2].strip()
                ret_desc['description'] = ret[3]

            if ret_desc:
                ret_data.append(ret_desc)

        return ret_data

    async def get(self):
        ret_data = []
        for route in router.routes:
            route_item = {}
            route_item['path'] = route.path
            route_item['description'] = self.parse_description(route.handler.__doc__)
            route_item['methods'] = []
            try:
                for m in self.documented_methods:
                    route_item['methods'].append(
                        {
                            m: {
                                "args": self.parse_args(getattr(route.handler, m).__doc__),
                                "body": self.parse_body(getattr(route.handler, m).__doc__),
                                "rets": self.parse_rets(getattr(route.handler, m).__doc__)
                            }
                        }
                    )
                ret_data.append(route_item)

            except Exception as e:
                print(e)

        return web.json_response(ret_data)
