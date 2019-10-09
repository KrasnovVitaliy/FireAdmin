from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db
import views.journal as journal
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()


def is_field_in_map(field, data_map, field_type):
    if not field in data_map:
        data_map[field] = field_type
    return data_map


def get_max_position(app_id, offer_type):
    result = db.session.execute(
        "SELECT max(offers_apps_relations.position)from offers_apps_relations inner join offers on offers_apps_relations.offer_id==offers.id where offers_apps_relations.app_id={} and offers.offer_type={} and offers.deleted is null;".format(
            int(app_id), int(offer_type)
        ))
    for row in result:
        return int(row[0])
    return 0


class OffersDuplicateView(web.View):
    @aiohttp_jinja2.template('offers/offers_duplicate.html')
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['offers_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])
        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        offer = db.session.query(db.Offers).filter_by(**filters).first()
        offer_data = offer.to_json()

        filters = {
            'deleted': None,
        }
        apps = db.session.query(db.Applications).filter_by(**filters).all()
        apps_data = [obj.to_json() for obj in apps]

        filters = {
            'offer_id': params['id']
        }

        offer_apps = db.session.query(db.OffersAppsRelations).filter_by(**filters).all()
        offer_apps_data = [obj.app_id for obj in offer_apps]

        offer_apps_creatives = db.session.query(db.OffersAppsCreatives).filter_by(**filters).all()
        offer_apps_creatives_data = {}
        for item in offer_apps_creatives:
            offer_apps_creatives_data[item.app_id] = item.creative_url

        offer_apps_orders = db.session.query(db.OffersAppsOrderUrls).filter_by(**filters).all()
        offer_apps_orders_data = {}
        for item in offer_apps_orders:
            offer_apps_orders_data[item.app_id] = item.order_url

        offer_apps_names = db.session.query(db.OffersAppsNames).filter_by(**filters).all()
        offer_apps_names_data = {}
        for item in offer_apps_names:
            offer_apps_names_data[item.app_id] = item.name

        offer_apps_summs = db.session.query(db.OffersAppsSumms).filter_by(**filters).all()
        offer_apps_summs_data = {}
        for item in offer_apps_summs:
            offer_apps_summs_data[item.app_id] = item.to_json()

        offer_apps_terms = db.session.query(db.OffersAppsTerms).filter_by(**filters).all()
        offer_apps_terms_data = {}
        for item in offer_apps_terms:
            offer_apps_terms_data[item.app_id] = item.to_json()

        offer_apps_percents = db.session.query(db.OffersAppsPercents).filter_by(**filters).all()
        offer_apps_percents_data = {}
        for item in offer_apps_percents:
            offer_apps_percents_data[item.app_id] = item.to_json()

        offers_state = None
        if 'state' in params:
            offers_state = params['state']

        current_app = None
        if 'current_app' in params:
            current_app = params['current_app']

        logger.debug("Offers overview get params: {}".format(params))

        return {
            'offers_types': avm.offers_types(),
            "permissions": user_permissions,
            'offer': offer_data,
            'apps': apps_data,
            'offer_apps': offer_apps_data,
            'offer_apps_creatives': offer_apps_creatives_data,
            'offer_apps_orders': offer_apps_orders_data,
            'offer_apps_names': offer_apps_names_data,
            'offer_apps_summs': offer_apps_summs_data,
            'offer_apps_terms': offer_apps_terms_data,
            'offer_apps_percents': offer_apps_percents_data,
            'offers_state': offers_state,
            'current_app': current_app,

            'active_menu_item': 'offers',
            'offers_type_id': int(offer_data['offer_type']),
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL
        }

    async def post(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['offers_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])
        params = self.request.rel_url.query

        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        offer = db.Offers()

        for field in post_data:
            if field in ['isActive', 'mir', 'visa', 'mastercard', 'qiwi', 'yandex', 'cash']:
                setattr(offer, field, 1)
            else:
                setattr(offer, field, post_data[field])

        if 'isActive' not in post_data:
            setattr(offer, 'isActive', 0)

        db.session.add(offer)
        db.session.commit()

        percent_app_data = {}
        terms_app_data = {}
        summs_app_data = {}

        for field in post_data:
            if "screen_app_" in field:
                offer_app_creative = db.OffersAppsCreatives(
                    app_id=field.replace('screen_app_', ''), offer_id=offer.id,
                    creative_url=post_data[field])
                db.session.add(offer_app_creative)

            elif "order_app_" in field:
                offer_app_order_url = db.OffersAppsOrderUrls(
                    app_id=field.replace('order_app_', ''), offer_id=offer.id,
                    order_url=post_data[field])
                db.session.add(offer_app_order_url)

            elif "name_app_" in field:
                offer_app_name = db.OffersAppsNames(
                    app_id=field.replace('screen_app_', ''), offer_id=offer.id,
                    name=post_data[field])
                db.session.add(offer_app_name)

            elif "percentPrefix_app_" in field:
                is_field_in_map(field=field.replace('percentPrefix_app_', ''),
                                data_map=percent_app_data, field_type={})
                percent_app_data[field.replace('percentPrefix_app_', '')]['percentPrefix'] = post_data[field]
            elif "percent_app_" in field:
                is_field_in_map(field=field.replace('percent_app_', ''),
                                data_map=percent_app_data, field_type={})
                percent_app_data[field.replace('percent_app_', '')]['percent'] = post_data[field]
            elif "percentPostfix_app_" in field:
                is_field_in_map(field=field.replace('percentPostfix_app_', ''),
                                data_map=percent_app_data, field_type={})
                percent_app_data[field.replace('percentPostfix_app_', '')]['percentPostfix'] = post_data[field]

            elif "summPrefix_app_" in field:
                is_field_in_map(field=field.replace('summPrefix_app_', ''),
                                data_map=summs_app_data, field_type={})
                summs_app_data[field.replace('summPrefix_app_', '')]['summPrefix'] = post_data[field]
            elif "summMin_app_" in field:
                is_field_in_map(field=field.replace('summMin_app_', ''),
                                data_map=summs_app_data, field_type={})
                summs_app_data[field.replace('summMin_app_', '')]['summMin'] = post_data[field]
            elif "summMid_app_" in field:
                is_field_in_map(field=field.replace('summMid_app_', ''),
                                data_map=summs_app_data, field_type={})
                summs_app_data[field.replace('summMid_app_', '')]['summMid'] = post_data[field]
            elif "summMax_app_" in field:
                is_field_in_map(field=field.replace('summMax_app_', ''),
                                data_map=summs_app_data, field_type={})
                summs_app_data[field.replace('summMax_app_', '')]['summMax'] = post_data[field]
            elif "summPostfix_app_" in field:
                is_field_in_map(field=field.replace('summPostfix_app_', ''),
                                data_map=summs_app_data, field_type={})
                summs_app_data[field.replace('summPostfix_app_', '')]['summPostfix'] = post_data[field]
            elif "termPrefix_app_" in field:
                is_field_in_map(field=field.replace('termPrefix_app_', ''),
                                data_map=terms_app_data, field_type={})
                terms_app_data[field.replace('termPrefix_app_', '')]['termPrefix'] = post_data[field]
            elif "termMin_app_" in field:
                is_field_in_map(field=field.replace('termMin_app_', ''),
                                data_map=terms_app_data, field_type={})
                terms_app_data[field.replace('termMin_app_', '')]['termMin'] = post_data[field]
            elif "termMid_app_" in field:
                is_field_in_map(field=field.replace('termMid_app_', ''),
                                data_map=terms_app_data, field_type={})
                terms_app_data[field.replace('termMid_app_', '')]['termMid'] = post_data[field]
            elif "termMax_app_" in field:
                is_field_in_map(field=field.replace('termMax_app_', ''),
                                data_map=terms_app_data, field_type={})
                terms_app_data[field.replace('termMax_app_', '')]['termMax'] = post_data[field]
            elif "termPostfix_app_" in field:
                is_field_in_map(field=field.replace('termPostfix_app_', ''),
                                data_map=terms_app_data, field_type={})
                terms_app_data[field.replace('termPostfix_app_', '')]['termPostfix'] = post_data[field]

            elif "app_" in field:
                app_id = field.replace('app_', '')

                max_position = get_max_position(app_id, offer.offer_type)
                offer_app_relation = db.OffersAppsRelations(
                    app_id=app_id, offer_id=offer.id, position=max_position + 1)

                db.session.add(offer_app_relation)

        for app_id in percent_app_data.keys():
            offer_app_percent = db.OffersAppsPercents(
                app_id=app_id, offer_id=offer.id,
                percent=percent_app_data[app_id]['percent'],
                percentPostfix=percent_app_data[app_id]['percentPostfix'],
                percentPrefix=percent_app_data[app_id]['percentPrefix'])
            db.session.add(offer_app_percent)

        for app_id in terms_app_data.keys():
            offer_app_term = db.OffersAppsTerms(
                app_id=app_id, offer_id=offer.id,
                termPostfix=terms_app_data[app_id]['termPostfix'],
                termMax=terms_app_data[app_id]['termMax'],
                termMid=terms_app_data[app_id]['termMid'],
                termMin=terms_app_data[app_id]['termMin'],
                termPrefix=terms_app_data[app_id]['termPrefix'])
            db.session.add(offer_app_term)

        for app_id in summs_app_data.keys():
            offer_app_summ = db.OffersAppsSumms(
                app_id=app_id, offer_id=offer.id,
                summPostfix=summs_app_data[app_id]['summPostfix'],
                summMax=summs_app_data[app_id]['summMax'],
                summMid=summs_app_data[app_id]['summMid'],
                summMin=summs_app_data[app_id]['summMin'],
                summPrefix=summs_app_data[app_id]['summPrefix'])
            db.session.add(offer_app_summ)

        db.session.commit()

        offers_state = None
        if 'state' in params:
            offers_state = params['state']

        current_app = None
        if 'current_app' in params:
            current_app = params['current_app']

        await journal.add_action(request=self.request, object_type=journal.OFFER_OBJECT, action=journal.DUPLICATE_ACTION,
                                 description=str(offer.to_json()))
        return web.HTTPFound('/offers?offers_type={}&state={}&current_app={}'.format(
            offer.offer_type, offers_state, current_app))
