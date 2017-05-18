# Haproxy Autodiscovery Exporter (hade)

auto discovery all haproxy docker containers by url, and run official `prometheus/haproxy-exporter` process for all haproxy nodes with `alias` by ip or dns name fo rancher, work with this [grafana dashboard](https://grafana.com/dashboards/364)

```yaml
version: '2'
services:
  haproxy_exporter:
    image: quay.io/prometheus/haproxy-exporter
    entrypoint:
      - /bin/sh
    command:
      - -c
      - cp /bin/haproxy_exporter /exec/haproxy_exporter
    volumes:
      - /exec
  hade:
    image: negash/hade
    volumes_from:
      - haproxy_exporter
    environment:
      - DOMAIN=http://haproxy.service.dc1.consul:9000/?stats;csv
    ports:
      - 9101:9101
```

if you use rancher add environment `RESOLVE_TYPE=rancher` for hade and example domain `DOMAIN=http://https.lb.rancher.internal:9000/?stats;csv`
