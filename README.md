= PACLDB =
Web frontend to the PACL Pan-Athapaskan Comparative Lexicon.

== Initial Setup ==

First, make sure you have a Python 3 virtual environment set up.

```
$ pip install virtualenv 
$ virtualenv ./venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

(Once set up, you need only run the `source` command to enter the virtual
environment.)

== Running locally ==

```
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run
```

== Deployment ==

TODO

== Monitoring ==

TODO

== Citations ==

[The Flask-User starter app](https://github.com/lingthio/Flask-User-starter-app) 
was useful.
