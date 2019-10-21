from aiohttp import web
import datetime
import logging
from config import Config
import db
import utils.firebase_client as fb_client
import views.journal as journal
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()


class OffersActionsView(web.View):
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['offers_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        offer = db.session.query(db.Offers).filter_by(**filters).first()
        if params['action'] == 'run':
            offer.isActive = 1
            await journal.add_action(request=self.request, object_type=journal.OFFER_OBJECT,
                                     action=journal.START_ACTION,
                                     description=str(offer.to_json()))
        elif params['action'] == 'stop':
            offer.isActive = 0
            await journal.add_action(request=self.request, object_type=journal.OFFER_OBJECT,
                                     action=journal.STOP_ACTION,
                                     description=str(offer.to_json()))
        elif params['action'] == 'delete':
            offer.deleted = datetime.datetime.now()
            await journal.add_action(request=self.request, object_type=journal.OFFER_OBJECT,
                                     action=journal.DELETE_ACTION,
                                     description=str(offer.to_json()))
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        return web.HTTPFound('offers?offers_type={}&current_app={}'.format(params['offer_type'], params['app_id']))


class OffersUpdateOrder(web.View):
    async def post(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['offers_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])
        params = self.request.rel_url.query
        data = await self.request.json()

        app_id = None
        if 'app_id' in params and params['app_id'] != None:
            app_id = params['app_id']

        offers_type_id = None
        if 'offers_type_id' in params and params['offers_type_id'] != None:
            offers_type_id = params['offers_type_id']

        country_id = None
        if 'country_id' in params and params['country_id'] != None:
            country_id = params['country_id']

        if country_id:
            for item in data:
                offer_position = db.session.query(db.OffersAppsCountriesPositions) \
                    .filter(db.OffersAppsCountriesPositions.app_id == app_id) \
                    .filter(db.OffersAppsCountriesPositions.offer_type_id == offers_type_id) \
                    .filter(db.OffersAppsCountriesPositions.offer_id == item['item_id']) \
                    .filter(db.OffersAppsCountriesPositions.country_id == country_id).first()
                if offer_position:
                    offer_position.position = item['position']
                else:
                    offer_position = db.OffersAppsCountriesPositions(app_id=app_id, offer_id=item['item_id'],
                                                                     offer_type_id=offers_type_id,
                                                                     country_id=country_id,
                                                                     position=item['position'])
                    db.session.add(offer_position)

                await journal.add_action(request=self.request, object_type=journal.OFFER_OBJECT,
                                         action=journal.REORDER_ACTION,
                                         description="app_id: {} offer_id: {} offer_type_id: {} country_id: {} position: {}".format(
                                             offer_position.app_id, offer_position.offer_id,
                                             offer_position.offer_type_id, offer_position.country_id,
                                             offer_position.position))

        else:
            for item in data:
                logger.debug("Post data: {}".format(item))
                offer_position = db.session.query(db.OffersAppsCountriesPositions).filter_by(app_id=app_id,
                                                                                             offer_id=item['item_id'],
                                                                                             offer_type_id=offers_type_id,
                                                                                             country_id=-1).first()

                if offer_position:
                    offer_position.position = item['position']
                else:
                    offer_position = db.OffersAppsCountriesPositions(app_id=app_id, offer_id=item['item_id'],
                                                                     offer_type_id=offers_type_id,
                                                                     country_id=-1,
                                                                     position=item['position'])
                    db.session.add(offer_position)
                print("CHANGE ORDER")
                await journal.add_action(request=self.request, object_type=journal.OFFER_OBJECT,
                                         action=journal.REORDER_ACTION,
                                         description="app_id: {} offer_id: {} offer_type_id: {} country_id: {} position: {}".format(
                                             offer_position.app_id, offer_position.offer_id,
                                             offer_position.offer_type_id, offer_position.country_id,
                                             offer_position.position))

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return web.HTTPOk()


class OffersUpdateComment(web.View):
    async def post(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['offers_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        data = await self.request.json()

        logger.debug("Post data: {}".format(data))
        offer = db.session.query(db.Offers).filter_by(id=data['item_id']).first()
        offer.comment = data['comment']

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        await journal.add_action(request=self.request, object_type=journal.OFFER_OBJECT,
                                 action=journal.UPDATE_COMMENT,
                                 description=str(offer.to_json()))
        return web.HTTPOk()


class OffersDynamicLink(web.View):
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['offers_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query
        try:
            if "app_id" not in params:
                return web.HTTPNoContent()
            app_id = int(params["app_id"])

            if "offer_id" not in params:
                return web.HTTPNoContent()
            offer_id = int(params["offer_id"])

            country_code = None
            if "country_code" in params:
                country_code = params["country_code"]

        except Exception as e:
            return web.HTTPNoContent()

        app = db.session.query(db.Applications).filter(db.Applications.id == app_id).first()
        offer = db.session.query(db.Offers).filter(db.Offers.id == offer_id).first()
        offer_type = db.session.query(db.OffersTypes).filter(db.OffersTypes.id == offer.offer_type).first()

        app_offers = fb_client.get_all(app.fb_id)

        offer_position = 0
        for item in app_offers[offer_type.name]:
            if int(offer.id) == int(item['id']):
                break
            offer_position += 1
        offer_link = "www.{}.ru/{}?id={}".format(app.fb_id, offer_type.name, offer_position)

        country_offer_link = "Страна не задана"
        if country_code:
            # country_offer_link = "http://www.{}.ru/offer_item/{}/{}/{}".format(
            #     app.fb_id, country_code, offer_type.name, offer_position)
            country_offer_link = "http://www.{}.ru/offer_item/{}/{}".format(
                app.fb_id, offer_type.name, offer_position)

        if "card" in offer_type.name:
            offer_position = 0
            for item in app_offers["cards"]:
                if int(offer.id) == int(item['id']):
                    break
                offer_position += 1
            old_link = "www.{}.ru/cards?id={}".format(app.fb_id, offer_position)
        else:
            old_link = offer_link

        rsp = {
            "old_link": old_link,
            "link": offer_link,
            "country_link": country_offer_link
        }

        return web.json_response(rsp)
