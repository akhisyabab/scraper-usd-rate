heroku config:set FLASK_ENV=production
heroku config:set DATABASE_URL='postgres://wwyoktuclytbip:dd06863a1f5693e4f39cd3c2414ea4bf50c68a10660cf5cf6041d4034004033d@ec2-184-72-236-3.compute-1.amazonaws.com:5432/d7clsj359ue66j'
heroku config:set APP_SETTINGS='project.config.ProductionConfig'