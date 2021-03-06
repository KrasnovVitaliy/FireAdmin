from aiohttp import web
from views.index import *
from views.auth.login import *
from views.auth.signup import *

from views.offers.offers_types import *
from views.offers.offers_list import *
from views.offers.offers_overview import *
from views.offers.offers_duplicate import *
from views.offers.offers_actions import *
from views.offers.offers_create import *

from views.apps.applications import *
from views.apps.apps_create import *
from views.apps.apps_overview import *
from views.apps.apps_duplicate import *
from views.apps.apps_db_json import *
from views.apps.apps_fb_db_json import *
from views.apps.apps_add_all_offers import *
from views.apps.apps_add_all_news import *
from views.apps.apps_actions import *
from views.apps.apps_ftp_update import *

from views.news.news_list import *
from views.news.news_create import *
from views.news.news_overview import *
from views.news.news_actions import *

from views.countries.countries import *
from views.countries.countries_overview import *
from views.countries.countries_create import *
from views.countries.countries_actions import *

from views.system import *
from views.journal import *

from views.config import *

config = Config()
# Define all routes and views here

path_to_static_folder = './static'
routes = [
    web.view('/', IndexView),

    web.view('/login', LoginView),
    web.view('/signup', SignupView),

    web.view('/offers_type', OffersTypesView),
    web.view('/offers', OffersView),
    web.view('/offers_overview', OffersOverviewView),
    web.view('/offers_actions', OffersActionsView),
    web.view('/offers_create', OffersCreateView),
    web.view('/offers_duplicate', OffersDuplicateView),
    web.view('/offers_update_order', OffersUpdateOrder),
    web.view('/offers_update_comment', OffersUpdateComment),
    web.view('/offers_dynamic_link', OffersDynamicLink),

    web.view('/applications', ApplicationsView),
    web.view('/applications_json', ApplicationsJsonView),
    web.view('/apps_create', AppsCreateView),
    web.view('/apps_overview', AppsOverviewView),
    web.view('/apps_duplicate', AppsDuplicateView),
    web.view('/apps_actions', AppsActionsView),
    web.view('/ftp_update', AppsFTPUpdate),

    web.view('/app_db_json', AppsDBJsonView),
    web.view('/app_fb_db_get', AppsFBDBGetView),
    web.view('/app_fb_db_load', AppsFBDBLoadView),
    web.view('/add_all_offers', AppsAddAllOffersView),
    web.view('/delete_all_offers', AppsDeleteAllOffersView),
    web.view('/add_all_news', AppsAddAllNewsView),
    web.view('/delete_all_news', AppsDeleteAllNewsView),

    web.view('/news', NewsView),
    web.view('/news_create', NewsCreateView),
    web.view('/news_overview', NewsOverviewView),
    web.view('/news_actions', NewsActionsView),
    web.view('/news_update_order', NewsUpdateOrder),
    web.view('/news_update_comment', NewsUpdateComment),
    web.view('/news_dynamic_link', NewsDynamicLink),

    web.view('/countries', CountriesView),
    web.view('/countries_overview', CountriesOverviewView),
    web.view('/countries_create', CountriesCreateView),
    web.view('/countries_actions', CountriesActionsView),

    web.view('/journal', JournalView),

    web.static('/static', path_to_static_folder, show_index=True),
    web.view('/config', ConfigsView),
]
