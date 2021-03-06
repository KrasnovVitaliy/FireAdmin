from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import views.apps.utils as apps_utils
import db
import views.journal as journal
from utils.check_permissions import is_permitted

logger = logging.getLogger(__name__)
config = Config()


class AppsCreateView(web.View):
    @aiohttp_jinja2.template('apps/apps_create.html')
    async def get(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        params = self.request.rel_url.query
        countries = db.session.query(db.Countries).all()
        countries_data = [obj.to_json() for obj in countries]

        return {
            "permissions": user_permissions,
            'offers_types': avm.offers_types(),
            'countries': countries_data,
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL
        }

    async def post(self, *args, **kwargs):
        user_permissions = is_permitted(self.request, ['apps_permission'])
        if not user_permissions:
            return web.HTTPMethodNotAllowed("", [])

        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        app = db.Applications()

        for field in post_data:
            if ("country_license_term_" not in field and
                    "country_license_init_term_" not in field):
                setattr(app, field, post_data[field])

            if "icon" in field:
                if post_data[field]:
                    file_name = apps_utils.save_file(post_data[field])
                    setattr(app, field, file_name)

        db.session.add(app)

        try:
            db.session.commit()
        except Exception as e:
            logger.error("Can not create app record in db: {}".format(e.__str__()))
            db.session.rollback()
            return web.HTTPInternalServerError()

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
            logger.error("Can not create app related records in db: {}".format(e.__str__()))
            db.session.rollback()
            return web.HTTPInternalServerError()

        await journal.add_action(request=self.request, object_type=journal.APP_OBJECT, action=journal.CREATE_ACTION,
                                 description=str(app.to_json()))

        return web.HTTPFound('/applications?')
