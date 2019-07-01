import db
from utils.data_fields_utils import prepare_object_data
from sqlalchemy import asc, desc
import re


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
            .filter(db.Offers.isActive == 1) \
            .order_by(asc(db.OffersAppsRelations.position)).all()
    else:
        results = db.session.query(db.OffersAppsRelations, db.Offers) \
            .filter(db.OffersAppsRelations.app_id == app.id) \
            .filter(db.OffersAppsRelations.offer_id == db.Offers.id) \
            .filter(db.Offers.deleted == None) \
            .filter(db.Offers.isActive == 1) \
            .order_by(asc(db.OffersAppsRelations.position)).all()

    offer_apps_creatives = db.session.query(db.OffersAppsCreatives).filter_by(**filters).all()
    offer_apps_creatives_data = {}
    for item in offer_apps_creatives:
        offer_apps_creatives_data[item.offer_id] = item.creative_url

    offer_apps_orders = db.session.query(db.OffersAppsOrderUrls).filter_by(**filters).all()
    offer_apps_orders_data = {}
    for item in offer_apps_orders:
        offer_apps_orders_data[item.offer_id] = item.order_url

    offer_apps_names = db.session.query(db.OffersAppsNames).filter_by(**filters).all()
    offer_apps_names_data = {}
    for item in offer_apps_names:
        offer_apps_names_data[item.offer_id] = item.name

    offer_apps_summs = db.session.query(db.OffersAppsSumms).filter_by(**filters).all()
    offer_apps_summs_data = {}
    for item in offer_apps_summs:
        offer_apps_summs_data[item.offer_id] = item.to_json()

    offer_apps_terms = db.session.query(db.OffersAppsTerms).filter_by(**filters).all()
    offer_apps_terms_data = {}
    for item in offer_apps_terms:
        offer_apps_terms_data[item.offer_id] = item.to_json()

    offer_apps_percents = db.session.query(db.OffersAppsPercents).filter_by(**filters).all()
    offer_apps_percents_data = {}
    for item in offer_apps_percents:
        offer_apps_percents_data[item.offer_id] = item.to_json()

    ret_data = {}
    for result in results:
        if result[1].isActive:
            offer_data = prepare_object_data(result[1].to_json())  # fields_to_str(trim_fields(result[1].to_json()))
            offer_data['order'] = offer_data['order'] + "?source={}".format(app.order_tracking_source)

            offer_type = db.session.query(db.OffersTypes).filter_by(id=result[1].offer_type).first()

            if offer_type.name not in ret_data:
                ret_data[offer_type.name] = []

            if ((int(offer_data['id']) in offer_apps_creatives_data) and
                    (offer_apps_creatives_data[int(offer_data['id'])] != '')):
                offer_data['screen'] = offer_apps_creatives_data[int(offer_data['id'])]

            if ((int(offer_data['id']) in offer_apps_names_data) and
                    (offer_apps_names_data[int(offer_data['id'])] != '')):
                offer_data['name'] = offer_apps_names_data[int(offer_data['id'])]

            if ((int(offer_data['id']) in offer_apps_orders_data) and
                    (offer_apps_orders_data[int(offer_data['id'])] != '')):
                offer_data['order'] = offer_apps_orders_data[int(offer_data['id'])]

            if ((int(offer_data['id']) in offer_apps_summs_data) and
                    (offer_apps_summs_data[int(offer_data['id'])] != '')):

                if offer_apps_summs_data[int(offer_data['id'])]['summPrefix'] != '':
                    offer_data['summPrefix'] = offer_apps_summs_data[int(offer_data['id'])]['summPrefix']

                if offer_apps_summs_data[int(offer_data['id'])]['summMin'] != '':
                    offer_data['summMin'] = offer_apps_summs_data[int(offer_data['id'])]['summMin']

                if offer_apps_summs_data[int(offer_data['id'])]['summMid'] != '':
                    offer_data['summMid'] = offer_apps_summs_data[int(offer_data['id'])]['summMid']
                if offer_apps_summs_data[int(offer_data['id'])]['summMax'] != '':
                    offer_data['summMax'] = offer_apps_summs_data[int(offer_data['id'])]['summMax']
                if offer_apps_summs_data[int(offer_data['id'])]['summPostfix'] != '':
                    offer_data['summPostfix'] = offer_apps_summs_data[int(offer_data['id'])]['summPostfix']

            if ((int(offer_data['id']) in offer_apps_terms_data) and
                    (offer_apps_terms_data[int(offer_data['id'])] != '')):

                if offer_apps_terms_data[int(offer_data['id'])]['termPrefix'] != '':
                    offer_data['termPrefix'] = offer_apps_terms_data[int(offer_data['id'])]['termPrefix']
                if offer_apps_terms_data[int(offer_data['id'])]['termMin'] != '':
                    offer_data['termMin'] = offer_apps_terms_data[int(offer_data['id'])]['termMin']
                if offer_apps_terms_data[int(offer_data['id'])]['termMid'] != '':
                    offer_data['termMid'] = offer_apps_terms_data[int(offer_data['id'])]['termMid']
                if offer_apps_terms_data[int(offer_data['id'])]['termMax'] != '':
                    offer_data['termMax'] = offer_apps_terms_data[int(offer_data['id'])]['termMax']
                if offer_apps_terms_data[int(offer_data['id'])]['termPostfix'] != '':
                    offer_data['termPostfix'] = offer_apps_terms_data[int(offer_data['id'])]['termPostfix']

            if ((int(offer_data['id']) in offer_apps_percents_data) and
                    (offer_apps_percents_data[int(offer_data['id'])] != '')):
                if offer_apps_percents_data[int(offer_data['id'])]['percentPrefix']:
                    offer_data['percentPrefix'] = offer_apps_percents_data[int(offer_data['id'])]['percentPrefix']
                if offer_apps_percents_data[int(offer_data['id'])]['percent']:
                    offer_data['percent'] = offer_apps_percents_data[int(offer_data['id'])]['percent']
                if offer_apps_percents_data[int(offer_data['id'])]['percentPostfix']:
                    offer_data['percentPostfix'] = offer_apps_percents_data[int(offer_data['id'])]['percentPostfix']

            # Adding additional fields for backward compatibility
            offer_data['summ'] = ""
            for field in ['summPrefix', 'summMin', 'summMid', 'summMax', 'summPostfix']:
                if field in offer_data:
                    offer_data['summ'] += " {}".format(offer_data[field])
            offer_data['summ'] = re.sub(' +', ' ', offer_data['summ'])

            offer_data['term'] = ""
            for field in ['termPrefix', 'termMin', 'termMid', 'termMax', 'termPostfix']:
                if field in offer_data:
                    offer_data['term'] += " {}".format(offer_data[field])
            offer_data['term'] = re.sub(' +', ' ', offer_data['term'])

            ret_data[offer_type.name].append(offer_data)

    filters = {
        'app_id': app.id,
    }
    if country_id:
        results = db.session.query(db.NewsAppsRelations, db.News, db.NewsCountriesRelations) \
            .filter_by(**filters) \
            .filter(db.NewsCountriesRelations.country_id == country_id) \
            .filter(db.NewsCountriesRelations.news_id == db.News.id) \
            .filter(db.NewsAppsRelations.news_id == db.News.id).order_by(asc(db.News.position)).all()
    else:
        results = db.session.query(db.NewsAppsRelations, db.News).filter_by(**filters).filter(
            db.NewsAppsRelations.news_id == db.News.id).order_by(asc(db.News.position)).all()

    # results = db.session.query(db.NewsAppsRelations, db.News).filter_by(**filters).filter(
    #     db.NewsAppsRelations.news_id == db.News.id).order_by(asc(db.News.position)).all()
    ret_data['news'] = []
    for result in results:
        if result[1].isActive:
            news_data = prepare_object_data(result[1].to_json())  # fields_to_str(trim_fields(result[1].to_json()))
            ret_data['news'].append(news_data)

    # Adding license terms
    ret_data['license_term'] = app.license_term

    cards = []
    if 'cards_debit' in ret_data:
        cards.extend(ret_data['cards_debit'])
    if 'cards_credit' in ret_data:
        cards.extend(ret_data['cards_credit'])
    if 'cards_installment' in ret_data:
        cards.extend(ret_data['cards_installment'])

    ret_data['cards'] = cards

    return ret_data


def gen_app_json(app):
    ret_data = get_offers_data(app)

    countries = db.session.query(db.Countries).all()
    for country in countries:
        ret_data[country.code] = get_offers_data(app, country_id=country.id)

    return ret_data
