from datetime import datetime
import io
import csv
import requests
from flask import Blueprint, redirect, url_for, render_template, make_response, Response
from sqlalchemy.sql import text

from project import db
from project.models.models import Records, TimeFetched
from project.utils.date import str2date, date2str

scraper_blueprint = Blueprint('scraper', __name__, template_folder='templates')


@scraper_blueprint.route('/', methods=['GET', 'POST'])
def home():
    records = Records.query.all()
    last_fetched = TimeFetched.query.filter_by(id=1).first()
    last_fetched = str2date(last_fetched.date, '%Y-%m-%d %H:%M:%S.%f')

    response = make_response(render_template('usd-rates.html', datas=records, last_fetched=date2str(last_fetched)))
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
        db.session.execute(text(
            'TRUNCATE TABLE timefetched RESTART IDENTITY;'
        ))

        now = datetime.utcnow()
        new_fetched = TimeFetched(str(now))
        db.session.add(new_fetched)

        for value in values:
            code = value['code']
            name = value['name']
            date = value['date']
            rate = value['inverseRate']
            new_record = Records(code, name, date, rate)
            db.session.add(new_record)
            db.session.commit()
    except Exception:
        db.session.rollback()

    return redirect(url_for('scraper.home'))


@scraper_blueprint.route('/csv', methods=['GET', 'POST'])
def csv_download():
    output = io.StringIO()
    writer = csv.writer(output)
    headers = ['code', 'name', 'date', 'rate']
    writer.writerow(headers)

    records = Records.query.all()
    for record in records:
        row = [record.code, record.name, record.date, record.rate]
        writer.writerow(row)

    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=usd-rates.csv"})
