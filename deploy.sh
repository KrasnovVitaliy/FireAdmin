rsync -uazP ./* root@51.158.176.243:/root/fireadmin2/
ssh root@51.158.176.243 'supervisorctl restart fireadmin2'
ssh root@51.158.176.243 'supervisorctl restart fireadmin_auth2'


#scp root@51.158.176.243:/root/fireadmin2.db ./