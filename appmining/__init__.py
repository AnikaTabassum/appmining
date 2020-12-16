"""
The flask application package.
"""

from os import environ
import os
import sys
from flask import Flask
from flask_cors import CORS
app= Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)
current_dir = os.path.dirname(os.path.realpath(__file__))
print("from init ",current_dir)
import appmining.controllers
class AppMining:
    host = environ.get('SERVER_HOST', '0.0.0.0')
    port = 5555
    
    
    try:
        port = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        port = 5555

    def __init__(self):
        temp="nothing important"

    def run(self):
        import RasaHost.controllers
        self.enable_logging()
        self.flask.run(self.host, self.port)

mine = AppMining()