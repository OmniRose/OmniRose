```
virtualenv .venv
. .venv/bin/activate
pip install -r tmc_rose/requirements.txt

createdb tmc_rose

cd tmc_rose
./manage.py migrate
```
