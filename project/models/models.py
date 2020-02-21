import json
from project import db

class Records(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String())
    name = db.Column(db.String())
    date = db.Column(db.String())
    rate = db.Column(db.String())

    def __init__(self, records):
        self.records = records

    def __repr__(self):
        return self.records

    def to_json(self):
        return json.loads(self.records)

