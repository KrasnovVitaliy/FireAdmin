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
        print("row[0] {}".format(row[0]))
        if row[0]:
            return int(row[0])
        else:
            return 0
    return 0


def get_max_country_offer_position(app_id, offer_type_id, country_id):
    result = db.session.execute(
        "SELECT max(position) from offers_apps_countries_positions where app_id={} and offer_type_id={} and country_id={};".format(
            int(app_id), int(offer_type_id), int(country_id)
        ))
    try:
        for row in result:
            return int(row[0])
    except:
        return 0
    return 0


class OffersCreateView(web.View):
    @aiohttp_jinja2.template('offers/offers_create.html')
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['offers_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query
        offer_data = {}
        if 'offers_type' in params:
            offer_data['offer_type'] = int(params['offers_type'])

        filters = {
            'deleted': None,
        }
        apps = db.session.query(db.Applications).filter_by(**filters).all()
        apps_data = [obj.to_json() for obj in apps]

        countries = db.session.query(db.Countries).all()
        countries_data = [obj.to_json() for obj in countries]
        return {
            'apps': apps_data,
            'offers_types': avm.offers_types(),
            "permissions": user_permissions,
            'offer': offer_data,
            'countries': countries_data,
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
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        percent_app_data = {}
        terms_app_data = {}
        summs_app_data = {}

        app_ids = []
        country_ids = []

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
                app_ids.append(app_id)

                position = get_max_country_offer_position(app_id=app_id, offer_type_id=offer.offer_type, country_id=-1)

                offer_position = db.OffersAppsCountriesPositions(app_id=app_id, offer_id=offer.id,
                                                                 offer_type_id=offer.offer_type,
                                                                 country_id=-1,
                                                                 position=position + 1)
                db.session.add(offer_position)

            elif "country_" in field:
                country_id = field.replace('country_', '')
                offer_country_relation = db.OffersCountriesRelations(
                    country_id=country_id, offer_id=offer.id)
                db.session.add(offer_country_relation)
                country_ids.append(country_id)

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

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        for app_id in app_ids:
            for country_id in country_ids:
                offer_position = db.session.query(db.OffersAppsCountriesPositions) \
                    .filter(db.OffersAppsCountriesPositions.offer_id == offer.id) \
                    .filter(db.OffersAppsCountriesPositions.offer_type_id == offer.offer_type) \
                    .filter(db.OffersAppsCountriesPositions.country_id == country_id) \
                    .filter(db.OffersAppsCountriesPositions.app_id == app_id).first()

                if not offer_position:
                    position = get_max_country_offer_position(app_id=app_id, offer_type_id=offer.offer_type,
                                                              country_id=country_id)
                    offer_position = db.OffersAppsCountriesPositions(app_id=app_id, offer_id=offer.id,
                                                                     offer_type_id=offer.offer_type,
                                                                     country_id=country_id,
                                                                     position=position + 1)
                    db.session.add(offer_position)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        await journal.add_action(request=self.request, object_type=journal.OFFER_OBJECT, action=journal.CREATE_ACTION,
                                 description=str(offer.to_json()))

        return web.HTTPFound('/offers?offers_type={}'.format(offer.offer_type))
