from aiohttp import web
import aiohttp_jinja2
import logging
import db
import datetime
import views.all_view_methods as avm
from config import Config
from utils.user_getter import get_user, get_session_user
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()

CREATE_ACTION = "создать"
DUPLICATE_ACTION = "копировать"
UPDATE_ACTION = "изменение"
DELETE_ACTION = "удалаить"
STOP_ACTION = "остановить"
START_ACTION = "запустить"
REORDER_ACTION = "изменение порядка"
UPDATE_COMMENT = "изменение комментария"

NEWS_OBJECT = "новость"
OFFER_OBJECT = "оффер"
APP_OBJECT = "приложение"

TIMEZONE_OFFSET = 3


async def add_action(object_type, action, description, request):
    user = await get_session_user(request)
    news_app_position = db.Journal(user_id=user['id'], object_type=object_type, action=action,
                                   description=str(description))
    db.session.add(news_app_position)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error("Can not create journal record: {}".format(e.__str__()))
    pass


class JournalView(web.View):
    @aiohttp_jinja2.template('journal.html')
    async def get(self, *args, **kwargs):
        user_permissions = await is_permitted(self.request, ['journal_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed()

        params = self.request.rel_url.query
        filters = {}
        for item in ['action', 'object_type']:
            if item in params and params[item] != '':
                filters[item] = params[item]

        date_filters = {}
        for item in ['start_date', 'end_date', ]:
            if item in params and params[item] != '':
                date_filters[item] = datetime.datetime.strptime(params[item].replace(" ", ""), '%m/%d/%Y')

        journal_sample = db.session.query(db.Journal).filter_by(**filters).order_by(db.Journal.id.desc())

        if 'start_date' in date_filters:
            journal_sample = journal_sample.filter(
                db.Journal.create_date >= date_filters['start_date'].strftime('%Y-%m-%d'))

        if 'end_date' in date_filters:
            journal_sample = journal_sample.filter(
                db.Journal.create_date < (date_filters['end_date'] + datetime.timedelta(days=1)).strftime('%Y-%m-%d'))

        limit = 10
        try:
            if 'limit' in params and params['limit'] != '':
                limit = int(params['limit'])
        except Exception as e:
            logger.error("Can not get limit argument: {}".format(e))

        journal_data = journal_sample.limit(limit).all()

        journal_items = []
        for obj in journal_data:
            journal_item = obj.to_json()
            journal_item['user'] = get_user(obj.user_id)
            journal_item['create_date'] = obj.create_date + datetime.timedelta(hours=TIMEZONE_OFFSET)
            journal_items.append(journal_item)

        return {
            "permissions": user_permissions,
            "offers_types": avm.offers_types(),
            'active_menu_item': 'journal',
            'journal_items': journal_items,
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL,
            'available_actions': [CREATE_ACTION, DUPLICATE_ACTION, UPDATE_ACTION, DELETE_ACTION, STOP_ACTION,
                                  START_ACTION, REORDER_ACTION, UPDATE_COMMENT],
            'available_objects': [NEWS_OBJECT, OFFER_OBJECT, APP_OBJECT],
            'selected_start_date': params["start_date"] if "start_date" in params else (
                    datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%m/%d/%Y'),
            'selected_end_date': params["end_date"] if "end_date" in params else (
                datetime.datetime.now().strftime('%m/%d/%Y')),
            'selected_action': params["action"] if "action" in params else "",
            'selected_object_type': params["object_type"] if "object_type" in params else "",
            'limit': limit,
        }
