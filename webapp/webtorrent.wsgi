#! /usr/bin/python3

import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/webtorrent/webapp")
from webtorrent import app as application
application.secret_key = ""
