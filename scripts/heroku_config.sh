heroku config:set FLASK_ENV=production
heroku config:set DATABASE_URL='postgres://gxmphkzjshvakb:ae36e4b3496c12116f772c6efa7052d8e991aa27717ae4e4b2288180a4c53725@ec2-35-172-85-250.compute-1.amazonaws.com:5432/d9a84p568lkmke'
heroku config:set APP_SETTINGS='project.config.ProductionConfig'