# PACLDB 
Web frontend to the PACL Pan-Athapaskan Comparative Lexicon.

## Initial Setup

First, make sure you have a Python 3 virtual environment set up.

```
$ pip install virtualenv 
$ virtualenv ./venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

(Once set up, you need only run the `source` command to enter the virtual
environment.)

### Initializing a fresh database

```
(venv) $ flask db init
(venv) $ flask db migrate -m 'initial schema'
```

This should generate a file in the root application directory called
`pacl.sqlite`.  If you have some CSV files that have been exported from
the original Excel dataset, you can import them with the `csvmigrate.py`
script.

```
$ scripts/csvmigrate.py pacl.sqlite \
    ~/Downloads/FLORA.csv ~/Downloads/TOOL.csv

Processing /Users/ntaylor/Downloads/FLORA.csv...
Processing /Users/ntaylor/Downloads/TOOL.csv...
All done!
Processed 23132 entries in 1.17 seconds
$ 
```

That script needs CSV files with certain headers.  See the docstring
in `scripts/csvmigrate.py` for details.

### Manually resetting the database from CSV

Use only if you're okay with throwing away the DB (because, for example,
you're going to reload it from CSV immediately):

```
(venv) $ rm pacl.sqlite
(venv) $ rm -r migrations
(venv) $ flask db init
(venv) $ flask db migrate -m 'initial schema'
(venv) $ python scripts/csvmigrate.py pacl.sqlite /path/to/pacl.csv
```

## Running locally 

```
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run
```

## Deployment 

TODO

## Monitoring 

TODO

## Citations 

[The Flask-User starter app](https://github.com/lingthio/Flask-User-starter-app) 
was useful.
[The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) was useful.
