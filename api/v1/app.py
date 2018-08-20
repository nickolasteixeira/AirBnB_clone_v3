#!/usr/bin/python3
from flask import Flask, Blueprint
from os import getenv
from models import storage
from api.v1.views import app_views
"""
Basic Flask App
"""


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown():
    """
    Closes session
    """
    storage.close()

if __name__ == "__main__":
    env_var = {'host': '0.0.0.0', 'port':'5000'}
    if getenv(HBNB_API_HOST):
        env_var[host] = getenv(HBNB_API_HOST)
    if getenv(HBNB_API_PORT):
        env_var[port] = getenv(HBNB_API_PORT)
    app.run(host=env_var[host], port=env_var[port], threaded=True)