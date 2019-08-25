# PACLDB 
Web frontend to the PACL Pan-Dene Comparative Lexicon.

## Initial Setup

Make sure postgres is installed.

```
$ brew install postgresql #OSX
```

Next, make sure you have a Python 3 virtual environment set up.

```
$ pip install virtualenv 
$ virtualenv ./venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

(Once set up, you need only run the `source` command to enter the virtual
environment.)

If you get linker errors installing psycopg2 on osx,
```
$ sudo xcode-select --install
$ pip install -r requirements.txt --global-option=build_ext --global-option="-I/usr/local/opt/openssl/include" --global-option="-L/usr/local/opt/openssl/lib"
```

### Initializing a fresh database

```
(venv) $ flask db init
(venv) $ flask db migrate -m 'initial schema'
```

### Manually resetting the database from CSV

Use only if you're okay with throwing away the DB (because, for example,
you're going to reload it from CSV immediately):

```
(venv) $ echo 'drop database pacl' | psql
(venv) $ echo 'create database pacl' | psql
(venv) $ rm -r migrations
(venv) $ flask db init
(venv) $ flask db migrate -m 'initial schema'
(venv) $ python scripts/csvmigrate.py 'postgres://localhost/pacl' /path/to/pacl.csv
```

To copy the database to production:

```
$ pgloader scripts/sqlmigrate # moves sqlite into local postgres
$ pg_dump -Fc --no-acl --no-owner -h localhost -U ntaylor pacl > db.dump
$ scp db.dump dijk:/srv/http/pub
$ heroku pg:backups:restore http://pub.dijkstracula.net/db.dump postgresql-colorful-21508
$ heroku ps:restart
```

## Running locally 

PACL runs either with the stock Flask server...
```
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run # default port 5000
```

...or with gunicorn for production.
```
$ gunicorn run # default port 8000
```

For account invite functionality, you'll need a local Sendgrid API key
exported.

## DB migration to production


## Deployment 

Deploying new code:
```
$ git push heroku master
```

## Monitoring 

TODO

## Citations 

- [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Flask Web Development (2nd ed)](https://www.oreilly.com/library/view/flask-web-development/9781491991725/)
