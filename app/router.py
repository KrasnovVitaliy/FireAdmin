from aiohttp import web
from views.index import *
from views.offers_types import *
from views.offers import *
from views.offers_overview import *
from views.offers_actions import *
from views.offers_create import *
from views.applications import *
from views.apps_create import *
from views.apps_overview import *

from views.config import *

config = Config()
# Define all routes and views here

path_to_static_folder = './static'
routes = [
    web.view('/', IndexView),
    web.view('/offers_type', OffersTypesView),
    web.view('/offers', OffersView),
    web.view('/offers_overview', OffersOverviewView),
    web.view('/offers_actions', OffersActionsView),
    web.view('/offers_create', OffersCreateView),
    web.view('/applications', ApplicationsView),
    web.view('/apps_create', AppsCreateView),
    web.view('/apps_overview', AppsOverviewView),

    web.static('/static', path_to_static_folder, show_index=True),
    web.view('/config', ConfigsView),
]
