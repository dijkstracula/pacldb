```
 ________  ________  ________                  ________  ___       ________     
|\   __  \|\   __  \|\   ___  \               |\   ___ \|\  \     |\   ____\    
\ \  \|\  \ \  \|\  \ \  \\ \  \  ____________\ \  \_|\ \ \  \    \ \  \___|    
 \ \   ____\ \   __  \ \  \\ \  \|\____________\ \  \ \\ \ \  \    \ \  \       
  \ \  \___|\ \  \ \  \ \  \\ \  \|____________|\ \  \_\\ \ \  \____\ \  \____  
   \ \__\    \ \__\ \__\ \__\\ \__\              \ \_______\ \_______\ \_______\
    \|__|     \|__|\|__|\|__| \|__|               \|_______|\|_______|\|_______|
                                                                                
          Web frontend to the PACL Pan-Dene Comparative Lexicon.
```

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

Use only if you're okay with throwing away the DB (because, for example,
you're going to reload it from CSV immediately):

```
(venv) $ flask db init
(venv) $ flask db migrate -m 'initial schema'
```

### Manually resetting the database from CSV


```
(venv) $ echo 'drop database pacl' | psql
(venv) $ echo 'create database pacl' | psql
(venv) $ rm -r migrations
(venv) $ flask db init
(venv) $ flask db migrate -m 'initial schema'
(venv) $ python scripts/csvmigrate.py 'postgres://localhost/pacl' /path/to/pacl.csv
```

Initialise an initial administration account:

```
(venv) ➜  pacldb git:(master) ✗ export FLASK_APP=pacl.py
(venv) ➜  pacldb git:(master) ✗ flask shell
Python 3.6.4 (default, Mar  1 2018, 18:36:42)
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)] on darwin
App: app [production]
Instance: /Users/ntaylor/code/pacldb/instance
>>> u = User(email="nbtaylor@gmail.com", password="hunter2", is_admin=True)
>>> db.session.add(u)
>>> db.session.commit()
>>> ^D
now exiting InteractiveConsole...
```

To prepopulate the home and about pages:

```
$ python scripts/mdimport.py 'postgres://localhost/pacl' ./markdowns
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

## Production

To open a remote shell:

```
$ DATABASE_URL=$(heroku config:get DATABASE_URL -a pan-dlc) flask shell
```

To make and download a db snapshot:

```
$ heroku pg:backups:capture --app pan-dlc
$ heroku pg:backups:download
```

### DB migrations

```
$ vim app/models.py
$ git add app/models.py
$ git commit -am 'your db migration description'

$ flask db migrate -m 'your db migration description'
$ less migrations/versions/deadbeeffoodcafe_migration_file.py
$ git add migrations

$ flask db upgrade # only for your local DB
$ git push
$ git push heroku master
```

## Deployment 

Deploying new code:

```
$ git push heroku master
```

## Monitoring 

- [Heroku dashboard](https://dashboard.heroku.com/apps/pan-dlc)
- [Heroku metrics](https://dashboard.heroku.com/apps/pan-dlc/metrics/web)

## Useful links

- [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Flask Web Development (2nd ed)](https://www.oreilly.com/library/view/flask-web-development/9781491991725/)
