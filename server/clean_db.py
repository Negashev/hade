import datetime

from server import db
from server.models import Zombie


def clean_db():
    too_old = datetime.datetime.today() - datetime.timedelta(minutes=30)
    to_delete = Zombie.query.filter(Zombie.date < too_old).all()
    if to_delete:
        for i in to_delete:
            db.session.delete(i)
        db.session.commit()


def truncate_db():
    to_delete = Zombie.query.all()
    if to_delete:
        for i in to_delete:
            db.session.delete(i)
        db.session.commit()
