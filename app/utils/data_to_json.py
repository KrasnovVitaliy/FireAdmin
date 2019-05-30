import db
from utils.data_fields_utils import prepare_object_data


def gen_app_json(app):
    filters = {
        'app_id': app.id,
    }
    results = db.session.query(db.OffersAppsRelations, db.Offers).filter_by(**filters).filter(
        db.OffersAppsRelations.offer_id == db.Offers.id).all()

    ret_data = {}
    for result in results:
        offer_data = prepare_object_data(result[1].to_json()) # fields_to_str(trim_fields(result[1].to_json()))
        offer_data['order'] = offer_data['order'] + "?source={}".format(app.order_tracking_source)

        offer_type = db.session.query(db.OffersTypes).filter_by(id=result[1].offer_type).first()

        if offer_type.name not in ret_data:
            ret_data[offer_type.name] = []

        ret_data[offer_type.name].append(offer_data)

    filters = {
        'app_id': app.id,
    }
    results = db.session.query(db.NewsAppsRelations, db.News).filter_by(**filters).filter(
        db.NewsAppsRelations.news_id == db.News.id).all()
    ret_data['news'] = []
    for result in results:
        news_data = prepare_object_data(result[1].to_json()) # fields_to_str(trim_fields(result[1].to_json()))
        ret_data['news'].append(news_data)

    # Adding license terms
    ret_data['license_term'] = app.license_term

    return ret_data
