import os
import socket
import re
import requests

from server import log, app


def get_dns(hostname, port):
    result = {}
    for i in socket.getaddrinfo(hostname, port):
        result[i[4][0]] = i[4][0]
    return result


def diff_ips_in_rancher(rancher_ips, haproxy_ips):
    for i in rancher_ips:
        if i in haproxy_ips:
            return i


def get_rancher():
    result = {}
    # find service, stack
    service, stack = re.sub('(\.rancher.internal)$', '', app.haproxy_url.hostname).split('.')
    # create RANCHER_PATH from {service} and {stack}
    RANCHER_PATH = os.getenv('RANCHER_PATH').format(service=service, stack=stack)

    haproxy_ips = get_dns(app.haproxy_url.hostname, app.haproxy_url.port)
    data = requests.get(f"{os.getenv('RANCHER_METADATA')}{RANCHER_PATH}", headers={'Accept': 'application/json'})
    for item in data.json():
        result[diff_ips_in_rancher(item['ips'], haproxy_ips)] = item['name']
    return result


def get_haproxy(resolve_type=os.getenv('RESOLVE_TYPE')):
    if resolve_type == 'rancher':
        app.haproxy = get_rancher()
    else:
        app.haproxy = get_dns(app.haproxy_url.hostname, app.haproxy_url.port)
    log.info(app.haproxy)
