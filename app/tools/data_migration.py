import sqlite_db
import pg_db
import json
from multiprocessing import Pool


def copy_data(src, dst):
    sqlite_data = sqlite_db.session.query(src).all()

    with open("{}.txt".format(str(dst)), "w") as err_file:
        for item in sqlite_data:
            parsed_item = item.to_json()
            app = dst()
            print(src)
            for field in parsed_item.keys():
                value = getattr(item, field) if getattr(item, field) != "" else None
                setattr(app, field, value)

            pg_db.session.add(app)
            try:
                pg_db.session.commit()
            except Exception as e:
                pg_db.session.rollback()
                print("Session roll back")

                err_file.write(item.to_json())
                err_file.write(json.dumps(parsed_item))
                err_file.write("\n========\n")
                err_file.write(e.__str__())
                err_file.write("\n========\n")
                err_file.write("\n")


def main():
    print("Started")
    pool = Pool(processes=5)

    pool.apply_async(copy_data, (sqlite_db.Applications, pg_db.Applications))
    pool.apply_async(copy_data, (sqlite_db.OffersTypes, pg_db.OffersTypes))
    pool.apply_async(copy_data, (sqlite_db.Offers, pg_db.Offers))
    pool.apply_async(copy_data, (sqlite_db.OffersAppsCountriesPositions, pg_db.OffersAppsCountriesPositions))
    pool.apply_async(copy_data, (sqlite_db.NewsAppsCountriesPositions, pg_db.NewsAppsCountriesPositions))
    pool.apply_async(copy_data, (sqlite_db.OffersAppsRelations, pg_db.OffersAppsRelations))
    pool.apply_async(copy_data, (sqlite_db.OffersAppsOrderUrls, pg_db.OffersAppsOrderUrls))
    pool.apply_async(copy_data, (sqlite_db.OffersAppsNames, pg_db.OffersAppsNames))
    pool.apply_async(copy_data, (sqlite_db.OffersAppsCreatives, pg_db.OffersAppsCreatives))
    pool.apply_async(copy_data, (sqlite_db.OffersAppsTerms, pg_db.OffersAppsTerms))
    pool.apply_async(copy_data, (sqlite_db.OffersAppsSumms, pg_db.OffersAppsSumms))
    pool.apply_async(copy_data, (sqlite_db.OffersAppsPercents, pg_db.OffersAppsPercents))
    pool.apply_async(copy_data, (sqlite_db.News, pg_db.News))
    pool.apply_async(copy_data, (sqlite_db.NewsAppsRelations, pg_db.NewsAppsRelations))
    pool.apply_async(copy_data, (sqlite_db.Countries, pg_db.Countries))
    pool.apply_async(copy_data, (sqlite_db.OffersCountriesRelations, pg_db.OffersCountriesRelations))
    pool.apply_async(copy_data, (sqlite_db.NewsCountriesRelations, pg_db.NewsCountriesRelations))
    pool.apply_async(copy_data, (sqlite_db.AppsCountriesTerms, pg_db.AppsCountriesTerms))
    pool.apply_async(copy_data, (sqlite_db.AppsCountriesInitTerms, pg_db.AppsCountriesInitTerms))
    pool.apply_async(copy_data, (sqlite_db.AppsCountriesRelations, pg_db.AppsCountriesRelations))
    pool.apply_async(copy_data, (sqlite_db.AppsDocumentsTypes, pg_db.AppsDocumentsTypes))
    pool.apply_async(copy_data, (sqlite_db.AppsDocuments, pg_db.AppsDocuments))
    pool.apply_async(copy_data, (sqlite_db.OffersAppsBrowsersTypes, pg_db.OffersAppsBrowsersTypes))
    pool.apply_async(copy_data, (sqlite_db.Journal, pg_db.Journal))

    pool.close()
    pool.join()

    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('applications', 'id'), MAX(id)) FROM applications;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('offers_types', 'id'), MAX(id)) FROM offers_types;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('offers', 'id'), MAX(id)) FROM offers;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('offers_apps_countries_positions', 'id'), MAX(id)) FROM offers_apps_countries_positions;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('news_apps_countries_positions', 'id'), MAX(id)) FROM news_apps_countries_positions;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('offers_apps_relations', 'id'), MAX(id)) FROM offers_apps_relations;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('offers_apps_order_urls', 'id'), MAX(id)) FROM offers_apps_order_urls;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('offers_apps_order_names', 'id'), MAX(id)) FROM offers_apps_order_names;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('offers_apps_creatives', 'id'), MAX(id)) FROM offers_apps_creatives;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('offers_apps_terms', 'id'), MAX(id)) FROM offers_apps_terms;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('offers_apps_summs', 'id'), MAX(id)) FROM offers_apps_summs;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('offers_apps_percents', 'id'), MAX(id)) FROM offers_apps_percents;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('news', 'id'), MAX(id)) FROM news;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('news_apps_relations', 'id'), MAX(id)) FROM news_apps_relations;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('countries', 'id'), MAX(id)) FROM countries;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('offers_countries_relations', 'id'), MAX(id)) FROM offers_countries_relations;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('news_countries_relations', 'id'), MAX(id)) FROM news_countries_relations;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('apps_countries_terms', 'id'), MAX(id)) FROM apps_countries_terms;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('apps_countries_init_terms', 'id'), MAX(id)) FROM apps_countries_init_terms;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('apps_countries_relations', 'id'), MAX(id)) FROM apps_countries_relations;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('apps_documents_types', 'id'), MAX(id)) FROM apps_documents_types;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('apps_documents', 'id'), MAX(id)) FROM apps_documents;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('offers_apps_browsers_types', 'id'), MAX(id)) FROM offers_apps_browsers_types;")
    pg_db.session.execute("SELECT pg_catalog.setval(pg_get_serial_sequence('journal', 'id'), MAX(id)) FROM journal;")

if __name__ == "__main__":
    main()
