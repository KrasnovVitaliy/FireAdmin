from aiohttp import web
import aiohttp_jinja2
import logging
from config import Config
import views.all_view_methods as avm
import db

logger = logging.getLogger(__name__)
config = Config()


class AppsOverviewView(web.View):
    @aiohttp_jinja2.template('apps/apps_overview.html')
    async def get(self, *args, **kwargs):
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

        return {
            'app': app_data,
            'offers_types': avm.offers_types(),
            'countries': countries_data,
            'app_country_terms': app_country_data,
            'auth_service_address': config.AUTH_SERVICE_ADDRESS
        }

    async def post(self, *args, **kwargs):
        params = self.request.rel_url.query
        post_data = await self.request.post()
        logger.debug("Received post data: {}".format(post_data))

        filters = {
            'id': params['id']
        }

        app = db.session.query(db.Applications).filter_by(**filters).first()
        db.session.query(db.AppsCountriesTerms).filter(db.AppsCountriesTerms.app_id == int(params['id'])).delete()

        for field in post_data:
            if "country_license_term_" in field:
                country_id = int(field.replace("country_license_term_", ""))

                app_country_term = db.AppsCountriesTerms(
                    app_id=int(params['id']),
                    country_id=int(country_id),
                    license_term=post_data[field]
                )
                db.session.add(app_country_term)

            else:
                setattr(app, field, post_data[field])

        db.session.add(app)
        db.session.commit()

        return web.HTTPFound('/applications?')
