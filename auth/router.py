from aiohttp import web
from views.api_tokens import *
from views.login import *
from views.logout import *
from views.users import *
from views.form_users import *
from views.roles import *
from views.docs import *
from views.config import *

# Define all routes and views here

config = Config()
path_to_static_folder = './static'
routes = [
    # Login
    web.view('/login', LoginView),
    web.view('/logout', LogoutView),

    # Users
    web.view('/users', UsersView),
    web.view('/form_users', FormUsersView),

    # Roles
    web.view('/roles', RolesView),

    # API Key
    web.view('/api_token', ApiTokenView),

    # System
]
if config.IS_DEBUG:
    routes.append(web.view('/doc', DocsView)),
    routes.append(web.view('/config', ConfigsView)),
