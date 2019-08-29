rsync -uazP ./* root@51.158.176.243:/root/fireadmin/
ssh root@51.158.176.243 'supervisorctl restart fireadmin'


#scp root@51.158.176.243:/root/fireadmin.db ./