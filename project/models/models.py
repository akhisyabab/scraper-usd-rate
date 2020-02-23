import json
from project import db

class Records(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String())
    name = db.Column(db.String())
    date = db.Column(db.String())
    rate = db.Column(db.String())

    def __init__(self, code, name, date, rate):
        self.code = code
        self.name = name
        self.date = date
        self.rate = rate

    def __repr__(self):
        return 'Record code = '.format(self.code)


class TimeFetched(db.Model):
    __tablename__ = 'timefetched'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String())

    def __init__(self, date):
        self.date = date

    def __repr__(self):
        return 'Last fetched = '.format(self.date)


