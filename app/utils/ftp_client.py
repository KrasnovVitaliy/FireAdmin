import logging
from ftplib import FTP

logger = logging.getLogger(__name__)


def cd_tree(ftp, ftp_dir):
    if ftp_dir != "":
        try:
            ftp.cwd(ftp_dir)

        except Exception as e:
            cd_tree(ftp, "/".join(ftp_dir.split("/")[:-1]))
            ftp.mkd(ftp_dir)
            ftp.cwd(ftp_dir)


def upload_to_ftp(ftp_host, ftp_path, path_to_local_file, ftp_username=None, ftp_password=None):
    logger.debug("Upload JSON to FTP host: {} with username {}".format(ftp_host, ftp_username))
    ftp = FTP(ftp_host)
    print(ftp.login(user=ftp_username, passwd=ftp_password))

    cd_tree(ftp, ftp_path)

    with open(path_to_local_file, 'rb') as fobj:
        logger.debug("Uploading local file {} file to FTP: {}".format(path_to_local_file, ftp_path))
        res = ftp.storbinary('STOR ' + path_to_local_file, fobj, 1024)
        logger.debug("Upload res: {}".format(res))


def download_from_ftp(ftp_host, ftp_path, path_to_local_file, ftp_username=None, ftp_password=None):
    logger.debug("Download JSON from FTP host: {} with username {}".format(ftp_host, ftp_username))
    ftp = FTP(ftp_host)
    print(ftp.login(user=ftp_username, passwd=ftp_password))

    with open(path_to_local_file, 'wb') as fobj:
        ftp.retrbinary('RETR %s' % ftp_path, fobj.write)
