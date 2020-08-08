"""
This script runs the SkaldBotAPI application using a development server.
"""

from os import environ
from SkaldBotAPI import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5555')
