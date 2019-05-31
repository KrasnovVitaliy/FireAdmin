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
from views.apps_db_json import *
from views.apps_fb_db_json import *
from views.apps_add_all_offers import *
from views.news import *
from views.news_create import *
from views.news_overview import *
from views.news_actions import *


from views.system import *


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
    web.view('/offers_update_order', OffersUpdateOrder),
    web.view('/offers_update_comment', OffersUpdateComment),

    web.view('/applications', ApplicationsView),
    web.view('/apps_create', AppsCreateView),
    web.view('/apps_overview', AppsOverviewView),

    web.view('/app_db_json', AppsDBJsonView),
    web.view('/app_fb_db_get', AppsFBDBGetView),
    web.view('/app_fb_db_load', AppsFBDBLoadView),
    web.view('/add_all_offers', AppsAddAllOffersView),
    web.view('/delete_all_offers', AppsDeleteAllOffersView),

    web.view('/news', NewsView),
    web.view('/news_create', NewsCreateView),
    web.view('/news_overview', NewsOverviewView),
    web.view('/news_actions', NewsActionsView),
    web.view('/news_update_order', NewsUpdateOrder),
    web.view('/news_update_comment', NewsUpdateComment),

    web.view('/system', SystemView),

    web.static('/static', path_to_static_folder, show_index=True),
    web.view('/config', ConfigsView),
]
