import requests

from server import app, log, db
from server.models import Zombie


def metrics_collector():
    metrics = {}
    for proc_id in app.prom.keys():
        port, ip, hostname = proc_id.split('|')
        data = requests.get(f"http://localhost:{port}/metrics")
        if data.status_code == 200:
            metrics[hostname] = data.text
        else:
            log.error(f'error response {proc_id}')
            db.session.add(Zombie(proc_id))
            db.session.commit()
    app.metrics = metrics
