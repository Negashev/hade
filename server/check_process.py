import datetime

from sqlalchemy import func

from server import db, log, app
from server.clean_db import truncate_db
from server.models import Zombie
from server.process_daemon import RunCmd


def check_process():
    minutes = 2
    too_old = datetime.datetime.today() - datetime.timedelta(minutes=minutes)
    zombies = db.session.query(Zombie.pid, func.count(Zombie.pid)) \
        .filter(Zombie.date > too_old) \
        .group_by(Zombie.pid).all()
    truncate = False
    for zombie in zombies:
        if zombie[1] > 3:
            truncate = True
            port, ip, hostname = zombie[0].split('|')
            try:
                app.prom[zombie[0]].stop()
            except Exception as e:
                log.error(e)
            log.info(f'restart {zombie[0]}')
            app.prom[zombie[0]] = RunCmd(port, ip)
            app.prom[zombie[0]].start()

    if truncate:
        truncate_db()
