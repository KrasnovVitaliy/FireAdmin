import db
from utils.user_getter import get_session_user_permissions


def offers_types():
    offers_types = db.session.query(db.OffersTypes).filter(db.OffersTypes.deleted == None).all()
    offers_types_data = [obj.to_json() for obj in offers_types]

    return offers_types_data
