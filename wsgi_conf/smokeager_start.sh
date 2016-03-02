#!/bin/bash

# !! DONOT run as ROOT !!

#uwsgi /home/aliasav/workspace/smokeager/wsgi_conf/smokeager_server.ini
uwsgi --http :8000 --chdir /home/aliasav/workspace/smokeager/ --wsgi-file smokeager/wsgi.py --master --pidfile=/tmp/uwsgi.pid\
--processes=1 --vacuum --daemonize=/tmp/uwsgi_smokeager_daemon

#ini file should be in the same folder from where this script is being run