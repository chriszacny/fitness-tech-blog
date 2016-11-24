from flask import Flask
from flask_flatpages import FlatPages


application = Flask(__name__)
flatpages = FlatPages(application)

import my_site.routes
