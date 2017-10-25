import os


class Config(object):
    JOBS = [
        {
            'id': 'get_servers',
            'func': 'server.get_haproxy:get_haproxy',
            'trigger': 'interval',
            'seconds': 10
        },
        {
            'id': 'process_daemon',
            'func': 'server.process_daemon:process_daemon',
            'trigger': 'interval',
            'seconds': 10
        },
        {
            'id': 'check_process',
            'func': 'server.check_process:check_process',
            'trigger': 'interval',
            'seconds': 10
        },
        {
            'id': 'clean_db',
            'func': 'server.clean_db:clean_db',
            'trigger': 'interval',
            'seconds': 20
        },
        {
            'id': 'metrics_collector',
            'func': 'server.metrics_collector:metrics_collector',
            'trigger': 'interval',
            'seconds': int(os.getenv('METRICS_COLLECTOR_INTERVAL', 5))
        }
    ]

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 1
    }
    SCHEDULER_TIMEZONE = "EST"
    SCHEDULER_API_ENABLED = True
