import copy
import os
import signal

import subprocess
import threading

from server import app, log


def process_daemon():
    # min port for prom haproxy explorer
    num = 19100

    prom_process = {}
    prom_port = {}
    app_haproxy = copy.deepcopy(app.haproxy)
    app_prom = copy.deepcopy(list(app.prom.keys()))
    for proc_id in app_prom:
        port, ip, hostname = proc_id.split('|')
        prom_process[ip] = hostname
        prom_port[ip] = int(port)
    log.info(f'prom_port {prom_port.values()}')

    # show diff
    if prom_process == app_haproxy:
        return
    # for new ports
    port = num
    # add prom haproxy explorer
    for add_candidate in app_haproxy.keys():
        if add_candidate in prom_process.keys():
            continue
        while port in prom_port.values():
            port += 1
            if port > 65535:
                break
        prom_port[add_candidate] = port
        new_thread = f'{port}|{add_candidate}|{app_haproxy[add_candidate]}'
        app.prom[new_thread] = RunCmd(port, add_candidate)
        app.prom[new_thread].start()
        log.info(f'add {port} {add_candidate} {app_haproxy[add_candidate]}')

    # remove prom haproxy explorer
    for remove_candidate in prom_process.keys():
        if remove_candidate in app_haproxy.keys():
            continue
        port = prom_port[remove_candidate]
        log.info(f'remove {port} {remove_candidate} {prom_process[remove_candidate]}')
        app.prom[f'{port}|{remove_candidate}|{prom_process[remove_candidate]}'].stop()
        del app.prom[f'{port}|{remove_candidate}|{prom_process[remove_candidate]}']


class RunCmd(threading.Thread):
    def __init__(self, exporter_port, ip):
        threading.Thread.__init__(self)
        self.exporter_port = exporter_port
        self.ip = ip

    def run(self):
        self.proc = subprocess.Popen([
            "/exec/haproxy_exporter",
            f"-haproxy.scrape-uri=http://{self.ip}:{app.haproxy_url.port}{app.haproxy_url.path}?{app.haproxy_url.query}",
            f"-web.listen-address=:{self.exporter_port}"
        ], shell=False)

    def stop(self):
        # Get the process id & try to terminate it gracefuly
        pid = self.proc.pid
        self.proc.terminate()

        # Check if the process has really terminated & force kill if not.
        try:
            os.kill(pid, 0)
            self.proc.kill()

            log.info("Forced kill")
        except OSError as e:
            log.info("Terminated gracefully")
