rsync -uazP ./* root@151.236.217.166:/root/fireadmin2/
ssh root@151.236.217.166 'supervisorctl restart fireadmin2'
ssh root@151.236.217.166 'supervisorctl restart fireadmin_auth2'
