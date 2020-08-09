"""
This script runs the SkaldBotAPI application using a development server.
"""

from os import environ
from SkaldBotAPI import app

if __name__ == '__main__':
    app.run(host='172.17.0.3', port='5555')
