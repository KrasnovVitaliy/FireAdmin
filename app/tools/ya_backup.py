# pip3 install yadisk
import yadisk

YA_ID = "2b30a559896c473e8621e24b5b751180"
YA_PASSWORD = "07632b30bd59455f972b8e7f1119a1be"
TOKEN = "AgAAAAAGKXB6AAaXHkFAH0kk0kumhC60RzQ2bC4"

YA_ID_E = "58efeaa2ad904e2db81ab1df0135fd0c"
YA_PASSWORD_E = "6891ab5f9836444d91828ec3194f3e31"
TOKEN_E = "AgAAAAAIavRJAAahMgDSkSnNGkq1u4eDUsfnxao"

DST_DIR = 'mobile_db_backup_old_fireadmin'


def upload_file(src_file, dst_file):
    try:
        ya = yadisk.YaDisk(YA_ID, YA_PASSWORD, TOKEN)
        ya.upload(src_file, dst_file)
    except Exception as e:
        print(e)


def upload_file_e(src_file, dst_file):
    try:
        ya = yadisk.YaDisk(YA_ID_E, YA_PASSWORD_E, TOKEN_E)
        ya.upload(src_file, dst_file)
    except Exception as e:
        print(e)


def backup_file(src_file, filename=None):
    if not filename:
        filename = src_file.split('/')[-1]
    upload_file(src_file, f"{DST_DIR}/{filename}")
    upload_file_e(src_file, f"{DST_DIR}/{filename}")


if __name__ == "__main__":
    backup_file("./db_restore.sh")
