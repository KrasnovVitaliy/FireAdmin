from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db
import views.apps.utils as apps_utils
from utils.check_permissions import is_permitted
import views.journal as journal

logger = logging.getLogger(__name__)
config = Config()


class AppsDuplicateView(web.View):
    @aiohttp_jinja2.template('apps/apps_duplicate.html')
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query

        filters = {
            'id': params['id']
        }

        app = db.session.query(db.Applications).filter_by(**filters).first()
        app_data = app.to_json()

        countries = db.session.query(db.Countries).all()
        countries_data = [obj.to_json() for obj in countries]

        app_country_terms = db.session.query(db.AppsCountriesTerms).filter(
            db.AppsCountriesTerms.app_id == int(params['id'])).all()
        app_country_data = {}

        for app_country_term in app_country_terms:
            app_country_data[app_country_term.country_id] = app_country_term

        app_country_init_terms = db.session.query(db.AppsCountriesInitTerms).filter(
            db.AppsCountriesInitTerms.app_id == int(params['id'])).all()
        app_country_init_terms_data = {}

        for app_country_init_term in app_country_init_terms:
            app_country_init_terms_data[app_country_init_term.country_id] = app_country_init_term

        app_countries_relation = db.session.query(db.AppsCountriesRelations) \
            .filter(db.AppsCountriesRelations.app_id == app.id).all()
        app_countries_relation_data = []
        for item in app_countries_relation:
            app_countries_relation_data.append(item.country_id)

        app_documents = db.session.query(db.AppsDocuments).filter(db.AppsDocuments.app_id == app.id).all()
        pos = 0
        app_documents_data = []
        for obj in app_documents:
            item = obj.to_json()
            item["position"] = pos
            app_documents_data.append(item)
            pos += 1

        apps_documents_types = db.session.query(db.AppsDocumentsTypes).all()
        apps_documents_types_data = [obj.to_json() for obj in apps_documents_types]

        return {
            "permissions": user_permissions,
            'app': app_data,
            'offers_types': avm.offers_types(),
            'countries': countries_data,
            'app_country_terms': app_country_data,
            'app_country_init_terms': app_country_init_terms_data,
            'app_countries_relation': app_countries_relation_data,
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL,
            'app_documents': app_documents_data,
            'apps_documents_types': apps_documents_types_data,
        }

    async def post(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        post_data = await self.request.post()
        app = db.Applications()

        src_app_id = None
        for field in post_data:
            if ("country_license_term_" not in field and
                    "country_license_init_term_" not in field and
                    "icon" not in field and "src_app_id" not in field):
                setattr(app, field, post_data[field])

            if "icon" in field:
                if post_data[field]:
                    file_name = apps_utils.save_file(post_data[field])
                    setattr(app, field, file_name)
            if "src_app_id" in field:
                src_app_id = int(post_data[field])

            if "show_docs" in field:
                app.show_docs = True

            if "hide_init_agreement" in field:
                app.hide_init_agreement = True

        db.session.add(app)
        try:
            db.session.commit()
        except Exception as e:
            logger.error(e)
            db.session.rollback()

        for field in post_data:
            if "country_license_term_" in field:
                country_id = int(field.replace("country_license_term_", ""))

                app_country_term = db.AppsCountriesTerms(
                    app_id=app.id,
                    country_id=int(country_id),
                    license_term=post_data[field]
                )
                db.session.add(app_country_term)

            if "country_license_init_term_" in field:
                country_id = int(field.replace("country_license_init_term_", ""))

                app_country_term = db.AppsCountriesInitTerms(
                    app_id=app.id,
                    country_id=int(country_id),
                    license_term=post_data[field]
                )
                db.session.add(app_country_term)
            elif "country_" in field:
                country_id = field.replace('country_', '')
                app_country_relation = db.AppsCountriesRelations(
                    country_id=country_id, app_id=app.id)
                db.session.add(app_country_relation)
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()

        try:
            db.session.commit()
        except Exception as e:
            logger.error(e)
            db.session.rollback()

        src_offers_relations = db.session.query(db.OffersAppsRelations).filter_by(app_id=src_app_id).all()
        for item in src_offers_relations:
            offer_app_relation = db.OffersAppsRelations(app_id=app.id, offer_id=item.offer_id, position=item.position)
            db.session.add(offer_app_relation)
        try:
            db.session.commit()
        except Exception as e:
            logger.error(e)
            db.session.rollback()

        src_news_relations = db.session.query(db.NewsAppsRelations).filter_by(app_id=src_app_id).all()
        for item in src_news_relations:
            news_app_relation = db.NewsAppsRelations(app_id=app.id, news_id=item.news_id, position=item.position)
            db.session.add(news_app_relation)
        try:
            db.session.commit()
        except Exception as e:
            logger.error(e)
            db.session.rollback()

        src_offers_position = db.session.query(db.OffersAppsCountriesPositions).filter_by(app_id=src_app_id).all()
        for item in src_offers_position:
            offers_app_position = db.OffersAppsCountriesPositions(app_id=app.id, offer_id=item.offer_id,
                                                                  position=item.position, country_id=item.country_id,
                                                                  offer_type_id=item.offer_type_id)
            db.session.add(offers_app_position)
        try:
            db.session.commit()
        except Exception as e:
            logger.error(e)
            db.session.rollback()

        src_news_position = db.session.query(db.NewsAppsCountriesPositions).filter_by(app_id=src_app_id).all()
        for item in src_news_position:
            news_app_position = db.NewsAppsCountriesPositions(app_id=app.id, news_id=item.news_id,
                                                                  position=item.position, country_id=item.country_id)
            db.session.add(news_app_position)
        try:
            db.session.commit()
        except Exception as e:
            logger.error(e)
            db.session.rollback()

        await journal.add_action(request=self.request, object_type=journal.APP_OBJECT, action=journal.DUPLICATE_ACTION,
                                 description=str(app.to_json()))
        return web.HTTPFound('/applications?')
