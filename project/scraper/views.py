import json
import requests
from flask import Blueprint, redirect, url_for, render_template, make_response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

from project import db
from project.models.models import Records

scraper_blueprint = Blueprint('scraper', __name__, template_folder='templates')


@scraper_blueprint.route('/', methods=['GET', 'POST'])
def home():
    records = Records.query.all()
    response = make_response(render_template('usd-rates.html', datas=records))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response

@scraper_blueprint.route('/fetch', methods=['GET', 'POST'])
def fetch():
    source = requests.get('http://www.floatrates.com/daily/usd.json')
    json_data = source.json()
    values = json_data.values()
    try:
        db.session.execute(text(
           'TRUNCATE TABLE records RESTART IDENTITY;'
        ))
        for value in values:
            code = value['code']
            name = value['name']
            date = value['date']
            rate = value['inverseRate']
            new_record = Records(code, name, date, rate)
            db.session.add(new_record)
            db.session.commit()
    except:
        db.session.rollback()

    return redirect(url_for('scraper.home'))