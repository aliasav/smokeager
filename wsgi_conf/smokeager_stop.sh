#!/bin/bash

# simple bash file to stop smokeager uwsgi server
# should be executed as the same user that was used to start the server

uwsgi --stop /tmp/uwsgi.pid # path to the uwsgi process pid file as mentioned in uwsgi.ini
