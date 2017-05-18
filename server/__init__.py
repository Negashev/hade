import os
from urllib.parse import urlparse

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from server.log import log
from server.apscheduler import Config

app = Flask(__name__)
from server.kill_all_processes import kill_all_processes
from server.log import log

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config.from_object(Config())

import server.env

db = SQLAlchemy(app)

app.haproxy = {}
app.prom = {}
app.haproxy_url = urlparse(os.getenv('DOMAIN'))
