import db
from utils.trim_fields import trim_fields


def gen_app_json(app):
    filters = {
        'app_id': app.id
    }
    results = db.session.query(db.OffersAppsRelations, db.Offers).filter_by(**filters).filter(
        db.OffersAppsRelations.offer_id == db.Offers.id).all()

    ret_data = {}
    for result in results:
        offer_data = trim_fields(result[1].to_json())
        offer_data['order'] = offer_data['order'] + "?source={}".format(app.order_tracking_source)

        offer_type = db.session.query(db.OffersTypes).filter_by(id=result[1].offer_type).first()

        if offer_type.name not in ret_data:
            ret_data[offer_type.name] = []
        ret_data[offer_type.name].append(offer_data)

    # Adding license terms
    ret_data['license_term'] = app.license_term

    return ret_data
