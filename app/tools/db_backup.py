import os
import datetime
import ya_backup

current_date = datetime.datetime.now().strftime('%d_%m_%y_%H')

ya_backup.backup_file("/root/fireadmin2.db", filename=f"fireadmin2_{current_date}.db")
ya_backup.backup_file("/root/fireadmin_auth2.db", filename=f"fireadmin_auth2_{current_date}.db")