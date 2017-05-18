import datetime

from server import db


class Zombie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.String, index=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)

    def __init__(self, pid):
        self.pid = pid

    def __repr__(self):
        return '<Zombie %r>' % self.pid

db.create_all()