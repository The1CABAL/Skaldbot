"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

from SkaldBotAPI.views import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

import SkaldBotAPI.views
