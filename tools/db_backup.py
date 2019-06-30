import os
import shutil
import datetime

srcdir = "/root"

current_date = datetime.datetime.now().strftime('%d_%m_%y_%H')
dstdir = "/root/db_backups/{}".format(current_date)

os.makedirs(dstdir)

for basename in os.listdir(srcdir):
    if basename.endswith('.db'):
        srcpathname = os.path.join(srcdir, basename)
        dstpathname = os.path.join(dstdir, basename)
        if os.path.isfile(srcpathname):
            shutil.copy2(srcpathname, dstpathname)
