import gspread
import csv
import io
import requests
from datetime import datetime

from flask import Blueprint, redirect, url_for, render_template, make_response, Response
from sqlalchemy.sql import text

from project import db
from project.models.models import Records, TimeFetched
from project.utils.date import str2date, date2str


from oauth2client.service_account import ServiceAccountCredentials


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
    # writer2 = csv.writer(open("usd-rates.csv", 'w')) # create csv file

    headers = ['code', 'name', 'date', 'rate']
    writer.writerow(headers)
    # writer2.writerow(headers)

    records = Records.query.all()
    for record in records:
        row = [record.code, record.name, record.date, record.rate]
        writer.writerow(row)
        # writer2.writerow(row)

    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=usd-rates.csv"})


@scraper_blueprint.route('/spreadsheet', methods=['GET', 'POST'])
def add_to_sheet():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('drive-public.json', scope)
    client = gspread.authorize(creds)

    # select spreadsheet
    sh = client.open('public-sheet')

    # # Delete worksheet
    # sh.del_worksheet(sh.worksheet("usd-rates"))
    # # Add worksheet
    # sh.add_worksheet(title="usd-rates", rows="100", cols="20")

    # # Select worksheet
    # worksheet = sh.worksheet("usd-rates")

    headers = ['Code', 'Name', 'Date', 'Rate']
    records = Records.query.all()
    datas = []
    datas.append(headers)
    for data in records:
        datas.append([data.code, data.name, data.date, data.rate])

    sh.values_update(
        '{}!A1'.format('usd-rates'),
        params={'valueInputOption': 'RAW'},
        body={'values': datas}
    )

    return redirect(url_for('scraper.home'))



