import json
import requests
from flask import Blueprint, redirect, url_for, render_template, make_response
from sqlalchemy.exc import IntegrityError

from project import db
from project.models.models import Records

scraper_blueprint = Blueprint('scraper', __name__, template_folder='templates')

@scraper_blueprint.route('/', methods=['GET', 'POST'])
def home():
    source = requests.get('http://www.floatrates.com/daily/usd.json')
    json_data = source.json()
    return render_template('usd-rates.html', datas=json_data.values())

@scraper_blueprint.route('/fetch', methods=['GET', 'POST'])
def fetch():
    source = requests.get('http://www.floatrates.com/daily/usd.json')
    json_data = source.json()
    return render_template('usd-rates.html', datas=json_data.values())