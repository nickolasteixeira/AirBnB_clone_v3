#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models import City
''' App_views routes'''

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def return_cities(state_id):
    '''return list of all the cities associated with the state_id'''
    all_cities = storage.all('City')
    new_cities = []
    for key, val in all_cities.items():
        obj = val.to_dict()
        if state_id == obj.get('state_id'):
            new_cities.append(obj)
    if len(new_cities) == 0:
        abort(404)
    return jsonify(new_cities)

@app_views.route('/cities/<city_id>', methods['GET'], strict_slashes=False)
def return_city(city_id):
    ''' returns the city object associated with the city_id'''
    
