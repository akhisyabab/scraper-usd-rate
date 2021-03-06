# USD RATES SCRAPER
1. The report came from www.floatrates.com json source
2. The report saved to database postgresql and google spreadsheet. Return to bootstrap table. Can export to csv file. 


## Table of contents
1. Get started on local
2. Deploy to heroku.

<hr>

## GET STARTED (Local):
#### create database and user on your local: 
```
CREATE DATABASE scraper_usd_rate;

CREATE USER scraperusdrateuser WITH password 'scraperusdratepassword';
GRANT ALL PRIVILEGES ON database scraper_usd_rate to scraperusdrateuser;
ALTER USER scraperusdrateuser SUPERUSER;
```


#### Setup:
```sh
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

#### upgrade db for init data:
```
$ source ./scripts/dev_env.sh
$ python manage.py db upgrade
```


#### Running:
```
$ source scripts/run.sh
```
**open localhost:5000*

#### Running prod: 
```
gunicorn --bind 0.0.0.0:80 manage:app
```
<hr><hr>

## Deploy (Heroku):

```sh
$ heroku login
$ heroku create app_name
$ git remote add heroku heroku_git_url
$ heroku addons:create heroku-postgresql:hobby-dev --app app_name
```

See database url with command:
```sh
$ heroku config --app app_name
```
Then Paste database URL to scripts/heroku_config.sh. Next commit your code changes and then:

```shell script
$ git push heroku master
$ source ./scripts/heroku_config.sh
$ heroku run python manage.py db upgrade
```
**Open app_name.herokuapp.com on your browser*

<hr><hr>

## NOTES
**Init report**

**Open "app_name.herokuapp.com/fetch" on your browser*


**Drop database**
```shell script
DROP DATABASE scraper_usd_rate;
```

**How migration**:
```
$ python manage.py db migrate
$ python manage.py db upgrade
```

**Heroku logs**:
```
$ heroku logs --tail
```

