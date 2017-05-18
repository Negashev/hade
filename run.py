import os

from flask_apscheduler import APScheduler
from prometheus_client.core import REGISTRY, GaugeMetricFamily
from prometheus_client.parser import text_string_to_metric_families
from prometheus_client import start_http_server

from server import app


class CustomCollector(object):
    def collect(self):
        for hostname in app.metrics.keys():
            for i in text_string_to_metric_families(app.metrics[hostname]):
                if i.samples[0][0] in ['process_cpu_seconds_total',
                                       'process_virtual_memory_bytes',
                                       'process_resident_memory_bytes',
                                       'process_start_time_seconds',
                                       'process_max_fds',
                                       'process_open_fds',
                                       'process_fake_namespace']:
                    continue
                for item in i.samples:
                    g = GaugeMetricFamily(item[0], i.documentation, labels=list(item[1].keys()) + ['alias'])
                    g.add_metric(list(item[1].values()) + [hostname], value=item[2])
                    yield g


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
