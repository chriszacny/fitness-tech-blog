from my_site import application
from my_site import flatpages

application.config.from_pyfile('settings.py', silent=True)
flatpages.init_app(application)
application.run(host=application.config['HOST'], debug=True)
