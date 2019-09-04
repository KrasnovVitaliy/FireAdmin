import time

APP_ICON_FOLDER = "./static/app_icons"


def save_file(file_field):
    # file_name = file_field.filename
    file_name = time.time()
    print("file_field")
    print(file_field)
    with open("{}/{}".format(APP_ICON_FOLDER, file_name), 'wb') as icon_file:
        icon_file.write(file_field.file.read())
    return file_name
