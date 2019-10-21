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


class AppsOverviewView(web.View):
    @aiohttp_jinja2.template('apps/apps_overview.html')
    async def get(self, *args, **kwargs):
        user_permissions = await is_permitted(self.request, ['apps_permission'])
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
            'app': app_data,
            "permissions": user_permissions,
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

        params = self.request.rel_url.query
        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        filters = {
            'id': params['id']
        }

        app = db.session.query(db.Applications).filter_by(**filters).first()
        db.session.query(db.AppsCountriesTerms).filter(db.AppsCountriesTerms.app_id == int(params['id'])).delete()
        db.session.query(db.AppsCountriesRelations).filter(
            db.AppsCountriesRelations.app_id == int(params['id'])).delete()

        app.browser_type = ""
        app_docs = {}
        app.show_docs = False
        app.hide_init_agreement = False

        for field in post_data:
            print("FIELD: ", field)
            if "country_license_term_" in field:
                country_id = int(field.replace("country_license_term_", ""))

                app_country_term = db.AppsCountriesTerms(
                    app_id=int(params['id']),
                    country_id=int(country_id),
                    license_term=post_data[field]
                )
                db.session.add(app_country_term)

            elif "country_init_license_term_" in field:
                country_id = int(field.replace("country_init_license_term_", ""))

                app_country_term = db.AppsCountriesInitTerms(
                    app_id=int(params['id']),
                    country_id=int(country_id),
                    license_term=post_data[field]
                )
                db.session.add(app_country_term)

            elif "country_" in field:
                country_id = field.replace('country_', '')
                app_country_relation = db.AppsCountriesRelations(
                    country_id=country_id, app_id=params['id'])
                db.session.add(app_country_relation)
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
            elif "apps_doc_" in field:
                num = field.split("_")[-1]
                if num not in app_docs:
                    app_docs[num] = {}

                app_docs[num][field.replace("_{}".format(num), '')] = post_data[field]
            elif "show_docs" in field:
                app.show_docs = True

            elif "hide_init_agreement" in field:
                app.hide_init_agreement = True

            elif "icon" in field:
                if post_data[field]:
                    file_name = apps_utils.save_file(post_data[field])
                    setattr(app, field, file_name)
            elif field in ["loans_item", "cards_item", "cards_credit_item", "cards_debit_item",
                           "cards_instalment_item", "credits_item", "news_item", "calculator_item"]:
                logger.debug("Set app attr: {}".format(field))
                setattr(app, field, True)

            else:
                setattr(app, field, post_data[field])

        db.session.add(app)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        documents_types = db.session.query(db.AppsDocumentsTypes).all()
        documents_types_data = {}
        for item in documents_types:
            documents_types_data[item.name.lower()] = item.id

        db.session.query(db.AppsDocuments).filter(db.AppsDocuments.app_id == app.id).delete()
        for key in app_docs.keys():
            app_doc = db.AppsDocuments(
                app_id=app.id,
                name=app_docs[key]['apps_doc_name'],
                url=app_docs[key]['apps_doc_url'],
                type=documents_types_data[app_docs[key]['apps_doc_type'].lower()],
            )

            db.session.add(app_doc)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()

        await journal.add_action(request=self.request, object_type=journal.APP_OBJECT, action=journal.UPDATE_ACTION,
                                 description=str(app.to_json()))
        return web.HTTPFound('/applications?')
