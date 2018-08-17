#!/usr/bin/python3
'''Basic Flask Application'''
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from models import Amenity
from models import City
from models import Place
from models import Review
from models import State
from models import User


@app_views.route('/status')
def return_status():
    ''' status '''
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def return_stats():
    ''' stats '''
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
