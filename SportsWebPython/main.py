"""
This script runs the SportsWebPython application using a development server.
"""
import sys
from os import environ
from SportsWebPython import app
import google

#gae_dir = google.__path__.append('C:\Program Files (x86)\Google\google_appengine')
#sys.path.insert(0, google.__path__[1]) # might not be necessary

#import google.appengine # now it's on your import path`
from google.appengine.ext.webapp.util import run_wsgi_app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    #app.run(HOST, PORT)
    run_wsgi_app(app)
