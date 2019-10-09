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
                setattr(app, field, getattr(item, field))

            pg_db.session.add(app)
            try:
                pg_db.session.commit()
            except Exception as e:
                pg_db.session.rollback()
                print("Session roll back")

                err_file.write(json.dumps(parsed_item))
                err_file.write("\n========\n")
                err_file.write(e.__str__())
                err_file.write("\n========\n")
                err_file.write("\n")


def main():
    print("Started")

    copy_data(sqlite_db.Applications, pg_db.Applications)
    copy_data(sqlite_db.OffersTypes, pg_db.OffersTypes)
    copy_data(sqlite_db.Offers, pg_db.Offers)
    copy_data(sqlite_db.OffersAppsCountriesPositions, pg_db.OffersAppsCountriesPositions)
    copy_data(sqlite_db.NewsAppsCountriesPositions, pg_db.NewsAppsCountriesPositions)
    copy_data(sqlite_db.OffersAppsRelations, pg_db.OffersAppsRelations)
    copy_data(sqlite_db.OffersAppsOrderUrls, pg_db.OffersAppsOrderUrls)
    copy_data(sqlite_db.OffersAppsNames, pg_db.OffersAppsNames)
    copy_data(sqlite_db.OffersAppsCreatives, pg_db.OffersAppsCreatives)
    copy_data(sqlite_db.OffersAppsTerms, pg_db.OffersAppsTerms)
    copy_data(sqlite_db.OffersAppsSumms, pg_db.OffersAppsSumms)
    copy_data(sqlite_db.OffersAppsPercents, pg_db.OffersAppsPercents)
    copy_data(sqlite_db.News, pg_db.News)
    copy_data(sqlite_db.NewsAppsRelations, pg_db.NewsAppsRelations)
    copy_data(sqlite_db.Countries, pg_db.Countries)
    copy_data(sqlite_db.OffersCountriesRelations, pg_db.OffersCountriesRelations)
    copy_data(sqlite_db.NewsCountriesRelations, pg_db.NewsCountriesRelations)
    copy_data(sqlite_db.AppsCountriesTerms, pg_db.AppsCountriesTerms)
    copy_data(sqlite_db.AppsCountriesInitTerms, pg_db.AppsCountriesInitTerms)
    copy_data(sqlite_db.AppsCountriesRelations, pg_db.AppsCountriesRelations)
    copy_data(sqlite_db.AppsDocumentsTypes, pg_db.AppsDocumentsTypes)
    copy_data(sqlite_db.AppsDocuments, pg_db.AppsDocuments)
    copy_data(sqlite_db.OffersAppsBrowsersTypes, pg_db.OffersAppsBrowsersTypes)
    copy_data(sqlite_db.Journal, pg_db.Journal)


if __name__ == "__main__":
    main()
