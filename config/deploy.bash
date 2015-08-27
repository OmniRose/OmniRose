#!/bin/bash

set -e

cd /home/omnirose/omnirose-website

. .venv/bin/activate

git pull

# check that the config files are not changed
diff -u config/nginx     /etc/nginx/sites-enabled/omnirose    || exit
diff -u config/uwsgi.ini /etc/uwsgi/apps-enabled/omnirose.ini || exit
diff -u omnirose/local_settings.py ~/local_settings.py        || exit

cd omnirose

pip install -q -r requirements.txt

./manage.py collectstatic --noinput
./manage.py migrate

echo
echo 'RUN "sudo service uwsgi restart" now'
echo
