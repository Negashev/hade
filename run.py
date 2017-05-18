import os

import requests
from flask_apscheduler import APScheduler
from prometheus_client.core import REGISTRY, GaugeMetricFamily
from prometheus_client.parser import text_string_to_metric_families
from prometheus_client import start_http_server

from server import app, db, log
from server.models import Zombie


class CustomCollector(object):
    def collect(self):
        for proc_id in app.prom.keys():
            port, ip, hostname = proc_id.split('|')
            data = requests.get(f"http://localhost:{port}/metrics")
            if data.status_code == 200:
                for i in text_string_to_metric_families(data.text):
                    if i.samples[0][0] in ['process_cpu_seconds_total',
                                           'process_virtual_memory_bytes',
                                           'process_resident_memory_bytes',
                                           'process_start_time_seconds',
                                           'process_max_fds',
                                           'process_open_fds',
                                           'process_fake_namespace']:
                        continue
                    g = GaugeMetricFamily(i.samples[0][0], i.documentation, labels=['alias'])
                    g.add_metric([hostname], value=i.samples[0][2])
                    yield g
            else:
                log.error(f'error response {proc_id}')
                db.session.add(Zombie(proc_id))
                db.session.commit()


REGISTRY.register(CustomCollector())

if __name__ == '__main__':
    # init APScheduler
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    host = os.getenv('HOST', '0.0.0.0')
    # init monitoring server
    start_http_server(int(os.getenv('PROM_PORT', 9101)), host)
    # init app
    app.run(host=host, port=int(os.getenv('PORT', 80)))
