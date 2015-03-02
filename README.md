```
virtualenv .venv
. .venv/bin/activate
pip install -r omnirose/requirements.txt

createdb omnirose

cd omnirose
./manage.py migrate
```
