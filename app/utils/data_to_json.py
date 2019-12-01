import db
from utils.data_fields_utils import prepare_object_data
from sqlalchemy import asc, desc
import re
import logging

logger = logging.getLogger(__name__)


def get_offer_country_position(offer_id, country_id, app_id):
    offer = db.session.query(db.OffersAppsCountriesPositions) \
        .filter(db.OffersAppsCountriesPositions.offer_id == offer_id) \
        .filter(db.OffersAppsCountriesPositions.country_id == country_id) \
        .filter(db.OffersAppsCountriesPositions.app_id == app_id).first()

    if offer:
        return offer.position
    return 0


def get_news_country_position(news_id, country_id, app_id):
    news_item = db.session.query(db.NewsAppsCountriesPositions) \
        .filter(db.NewsAppsCountriesPositions.news_id == news_id) \
        .filter(db.NewsAppsCountriesPositions.country_id == country_id) \
        .filter(db.NewsAppsCountriesPositions.app_id == app_id).first()

    if news_item:
        return news_item.position
    return 0


def get_offers_data(app, country_id=None):
    filters = {
        'app_id': app.id,
    }

    if country_id:
        results = db.session.query(db.OffersAppsRelations, db.Offers, db.OffersCountriesRelations) \
            .filter(db.OffersAppsRelations.app_id == app.id) \
            .filter(db.OffersCountriesRelations.country_id == country_id) \
            .filter(db.OffersCountriesRelations.offer_id == db.Offers.id) \
            .filter(db.OffersAppsRelations.offer_id == db.Offers.id) \
            .filter(db.Offers.deleted == None) \
            .filter(db.Offers.isActive == 1).all()
        # .order_by(asc(db.OffersAppsRelations.position))
    else:
        results = db.session.query(db.OffersAppsRelations, db.Offers) \
            .filter(db.OffersAppsRelations.app_id == app.id) \
            .filter(db.OffersAppsRelations.offer_id == db.Offers.id) \
            .filter(db.Offers.deleted == None) \
            .filter(db.Offers.isActive == 1) \
            .order_by(asc(db.OffersAppsRelations.position)).all()

    offer_apps_creatives = db.session.query(
        db.OffersAppsCreatives).filter_by(**filters).all()
    offer_apps_creatives_data = {}
    for item in offer_apps_creatives:
        offer_apps_creatives_data[item.offer_id] = item.creative_url

    offer_apps_orders = db.session.query(
        db.OffersAppsOrderUrls).filter_by(**filters).all()
    offer_apps_orders_data = {}
    for item in offer_apps_orders:
        offer_apps_orders_data[item.offer_id] = item.order_url

    offer_apps_names = db.session.query(
        db.OffersAppsNames).filter_by(**filters).all()
    offer_apps_names_data = {}
    for item in offer_apps_names:
        offer_apps_names_data[item.offer_id] = item.name

    offer_apps_summs = db.session.query(
        db.OffersAppsSumms).filter_by(**filters).all()
    offer_apps_summs_data = {}
    for item in offer_apps_summs:
        offer_apps_summs_data[item.offer_id] = item.to_json()

    offer_apps_terms = db.session.query(
        db.OffersAppsTerms).filter_by(**filters).all()
    offer_apps_terms_data = {}
    for item in offer_apps_terms:
        offer_apps_terms_data[item.offer_id] = item.to_json()

    offer_apps_percents = db.session.query(
        db.OffersAppsPercents).filter_by(**filters).all()
    offer_apps_percents_data = {}
    for item in offer_apps_percents:
        offer_apps_percents_data[item.offer_id] = item.to_json()

    offers_apps_browser_types = db.session.query(
        db.OffersAppsBrowsersTypes).filter_by(**filters).all()
    offers_apps_browser_types_data = {}
    for item in offers_apps_browser_types:
        offers_apps_browser_types_data[item.offer_id] = item.to_json()

    ret_data = {}
    for result in results:
        if result[1].isActive:
            # fields_to_str(trim_fields(result[1].to_json()))
            offer_data = prepare_object_data(result[1].to_json())
            offer_data['order'] = offer_data['order'] + \
                                  "?source={}".format(app.order_tracking_source)

            offer_type = db.session.query(db.OffersTypes).filter_by(
                id=result[1].offer_type).first()

            if offer_type.name not in ret_data:
                ret_data[offer_type.name] = []

            if ((int(offer_data['id']) in offer_apps_creatives_data) and
                    (offer_apps_creatives_data[int(offer_data['id'])] != '')):
                offer_data['screen'] = offer_apps_creatives_data[int(
                    offer_data['id'])]

            if ((int(offer_data['id']) in offer_apps_names_data) and
                    (offer_apps_names_data[int(offer_data['id'])] != '')):
                offer_data['name'] = offer_apps_names_data[int(
                    offer_data['id'])]

            if ((int(offer_data['id']) in offer_apps_orders_data) and
                    (offer_apps_orders_data[int(offer_data['id'])] != '')):
                offer_data['order'] = offer_apps_orders_data[int(
                    offer_data['id'])]

            if ((int(offer_data['id']) in offer_apps_summs_data) and
                    (offer_apps_summs_data[int(offer_data['id'])] != '')):

                if offer_apps_summs_data[int(offer_data['id'])]['summPrefix'] != '':
                    offer_data['summPrefix'] = offer_apps_summs_data[int(
                        offer_data['id'])]['summPrefix']

                if offer_apps_summs_data[int(offer_data['id'])]['summMin'] != '':
                    offer_data['summMin'] = str(
                        offer_apps_summs_data[int(offer_data['id'])]['summMin'])

                if offer_apps_summs_data[int(offer_data['id'])]['summMid'] != '':
                    offer_data['summMid'] = str(
                        offer_apps_summs_data[int(offer_data['id'])]['summMid'])
                if offer_apps_summs_data[int(offer_data['id'])]['summMax'] != '':
                    offer_data['summMax'] = str(
                        offer_apps_summs_data[int(offer_data['id'])]['summMax'])
                if offer_apps_summs_data[int(offer_data['id'])]['summPostfix'] != '':
                    offer_data['summPostfix'] = offer_apps_summs_data[int(
                        offer_data['id'])]['summPostfix']

            if ((int(offer_data['id']) in offer_apps_terms_data) and
                    (offer_apps_terms_data[int(offer_data['id'])] != '')):

                if offer_apps_terms_data[int(offer_data['id'])]['termPrefix'] != '':
                    offer_data['termPrefix'] = offer_apps_terms_data[int(
                        offer_data['id'])]['termPrefix']
                if offer_apps_terms_data[int(offer_data['id'])]['termMin'] != '':
                    offer_data['termMin'] = offer_apps_terms_data[int(
                        offer_data['id'])]['termMin']
                if offer_apps_terms_data[int(offer_data['id'])]['termMid'] != '':
                    offer_data['termMid'] = offer_apps_terms_data[int(
                        offer_data['id'])]['termMid']
                if offer_apps_terms_data[int(offer_data['id'])]['termMax'] != '':
                    offer_data['termMax'] = offer_apps_terms_data[int(
                        offer_data['id'])]['termMax']
                if offer_apps_terms_data[int(offer_data['id'])]['termPostfix'] != '':
                    offer_data['termPostfix'] = offer_apps_terms_data[int(
                        offer_data['id'])]['termPostfix']

            if ((int(offer_data['id']) in offer_apps_percents_data) and
                    (offer_apps_percents_data[int(offer_data['id'])] != '')):
                if offer_apps_percents_data[int(offer_data['id'])]['percentPrefix']:
                    offer_data['percentPrefix'] = offer_apps_percents_data[int(
                        offer_data['id'])]['percentPrefix']
                if offer_apps_percents_data[int(offer_data['id'])]['percent']:
                    offer_data['percent'] = offer_apps_percents_data[int(
                        offer_data['id'])]['percent']
                if offer_apps_percents_data[int(offer_data['id'])]['percentPostfix']:
                    offer_data['percentPostfix'] = offer_apps_percents_data[int(
                        offer_data['id'])]['percentPostfix']

            # Adding additional fields for backward compatibility
            offer_data['summ'] = ""
            for field in ['summPrefix', 'summMin', 'summMid', 'summMax', 'summPostfix']:
                if field in offer_data:
                    offer_data['summ'] += "{} ".format(offer_data[field])
            offer_data['summ'] = re.sub(' +', ' ', offer_data['summ'])

            # Removing spaces in the begin and end of string
            if offer_data['summ'][-1] == " ":
                offer_data['summ'] = offer_data['summ'][:-1]
            if len(offer_data['summ']) > 1 and offer_data['summ'][0] == " ":
                offer_data['summ'] = offer_data['summ'][1:]

            offer_data['term'] = ""
            for field in ['termPrefix', 'termMin', 'termMid', 'termMax', 'termPostfix']:
                if field in offer_data:
                    offer_data['term'] += "{} ".format(offer_data[field])
            offer_data['term'] = re.sub(' +', ' ', offer_data['term'])

            # Removing spaces in the begin and end of string
            if offer_data['term'][-1] == " ":
                offer_data['term'] = offer_data['term'][:-1]

            if len(offer_data['term']) > 1 and offer_data['term'][0] == " ":
                offer_data['term'] = offer_data['term'][1:]

            # Updating empty scores "" to "0"
            if offer_data['score'] == "":
                offer_data['score'] = "0"

            ret_data[offer_type.name].append(offer_data)

            if country_id:
                offer_data['position'] = get_offer_country_position(
                    offer_id=offer_data['id'], country_id=country_id, app_id=app.id)
            else:
                offer_data['position'] = get_offer_country_position(
                    offer_id=offer_data['id'], country_id=-1, app_id=app.id)

            # Updating offer browser type
            offer_data['browserType'] = offer_data['browser_type']
            if int(offer_data['id']) in offers_apps_browser_types_data:
                offer_data['browserType'] = offers_apps_browser_types_data[int(
                    offer_data['id'])]['browser_type']
            if app.browser_type and app.browser_type != "":
                offer_data['browserType'] = app.browser_type

            if 'browser_type' in offer_data:
                del offer_data['browser_type']

    filters = {
        'app_id': app.id,
    }
    if country_id:
        results = db.session.query(db.NewsAppsRelations, db.News, db.NewsCountriesRelations) \
            .filter_by(**filters) \
            .filter(db.NewsCountriesRelations.country_id == country_id) \
            .filter(db.NewsCountriesRelations.news_id == db.News.id) \
            .filter(db.NewsAppsRelations.news_id == db.News.id).all()
    else:
        results = db.session.query(db.NewsAppsRelations, db.News).filter_by(**filters).filter(
            db.NewsAppsRelations.news_id == db.News.id).order_by(asc(db.News.position)).all()

    ret_data['news'] = []
    for result in results:
        if result[1].isActive:
            news_data = prepare_object_data(result[1].to_json())

            if country_id:
                news_data['position'] = get_news_country_position(
                    news_id=news_data['id'], country_id=country_id, app_id=app.id)
            else:
                news_data['position'] = get_news_country_position(
                    news_id=news_data['id'], country_id=-1, app_id=app.id)

            ret_data['news'].append(news_data)

    for key in ret_data.keys():
        ret_data[key] = sorted(ret_data[key], key=lambda k: k['position'])

    app_country_terms = db.session.query(db.AppsCountriesTerms) \
        .filter(db.AppsCountriesTerms.app_id == app.id) \
        .filter(db.AppsCountriesTerms.country_id == country_id) \
        .first()

    app_country_init_terms = db.session.query(db.AppsCountriesInitTerms) \
        .filter(db.AppsCountriesInitTerms.app_id == app.id) \
        .filter(db.AppsCountriesInitTerms.country_id == country_id) \
        .first()

    if app_country_init_terms:
        if app_country_terms:
            ret_data['license_term'] = app_country_terms.license_term
            ret_data['init_license_term'] = app_country_init_terms.license_term
        else:
            ret_data['license_term'] = app.license_term
            ret_data['init_license_term'] = app.init_license_term
    else:
        ret_data['license_term'] = app.license_term
        ret_data['init_license_term'] = app.init_license_term

    ret_data["documents"] = []
    results = db.session.query(db.AppsDocuments, db.AppsDocumentsTypes) \
        .filter(db.AppsDocuments.app_id == app.id) \
        .filter(db.AppsDocuments.type == db.AppsDocumentsTypes.id) \
        .all()

    for result in results:
        ret_data["documents"].append(
            {
                "name": result[0].name,
                "url": result[0].url,
                "type": result[1].name,
            }
        )

    # Adding cards
    cards = []
    if 'cards_debit' in ret_data:
        cards.extend(ret_data['cards_debit'])
    if 'cards_credit' in ret_data:
        cards.extend(ret_data['cards_credit'])
    if 'cards_installment' in ret_data:
        cards.extend(ret_data['cards_installment'])

    ret_data['cards'] = cards

    ret_data['showDocs'] = "1" if app.show_docs else "0"
    ret_data['hideInitAgreement'] = "1" if app.hide_init_agreement else "0"

    return ret_data


def get_app_countrie(app):
    countries = []
    results = db.session.query(db.AppsCountriesRelations, db.Countries) \
        .filter(db.AppsCountriesRelations.app_id == app.id) \
        .filter(db.AppsCountriesRelations.country_id == db.Countries.id).all()
    for result in results:
        countries.append(
            {
                'id': str(result[1].id),
                'code': result[1].code,
                'name': result[1].name,
                'icon': result[1].icon,
            }
        )
    return countries


def get_app_config(app, country_id=None):
    result = db.session.query(db.Applications) \
        .filter(db.Applications.id == app.id).first()

    configs = {
        'loans_item': "1" if result.loans_item else "0",
        'credits_item': "1" if result.credits_item else "0",
        'news_item': "1" if result.news_item else "0",
        'cards_item': "1" if result.cards_item else "0",
        'cards_credit_item': "1" if result.cards_credit_item else "0",
        'cards_debit_item': "1" if result.cards_debit_item else "0",
        'cards_installment_item': "1" if result.cards_instalment_item else "0",
        'calculator_item': "1" if result.calculator_item else "0",
        'history_item': "1" if result.history_item else "0",
        'hide_order_offer': "1" if result.hide_order_offer else "0"
    }

    results = db.session.query(db.AppsCountriesVisibleOffers, db.Countries).filter(
        db.AppsCountriesVisibleOffers.app_id == app.id).filter(
        db.AppsCountriesVisibleOffers.country_id == db.Countries.id
    ).all()

    for result in results:
        configs[result[1].code] = {
            'loans_item': "1" if result[0].loans_item else "0",
            'credits_item': "1" if result[0].credits_item else "0",
            'news_item': "1" if result[0].news_item else "0",
            'cards_item': "1" if result[0].cards_item else "0",
            'cards_credit_item': "1" if result[0].cards_credit_item else "0",
            'cards_debit_item': "1" if result[0].cards_debit_item else "0",
            'cards_installment_item': "1" if result[0].cards_instalment_item else "0",
            'calculator_item': "1" if result[0].calculator_item else "0",
            'history_item': "1" if result[0].history_item else "0",
            'hide_order_offer': "1" if result[0].hide_order_offer else "0"
        }
    return configs


def gen_app_json(app):
    ret_data = get_offers_data(app)

    countries = db.session.query(db.Countries).all()
    for country in countries:
        ret_data[country.code] = get_offers_data(app, country_id=country.id)

    ret_data['countries'] = get_app_countrie(app)
    ret_data['app_config'] = get_app_config(app)
    return ret_data
