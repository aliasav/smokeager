# restart smokeager server

# activate virtual env
source /home/aliasav/virtualenvs/smokeager/bin/activate

# stop smokeager uwsgi server
source /home/aliasav/workspace/smokeager/wsgi_conf/smokeager_stop.sh

# add delay
sleep 2

# start smokeager uwsgi server
source /home/aliasav/workspace/smokeager/wsgi_conf/smokeager_start.sh