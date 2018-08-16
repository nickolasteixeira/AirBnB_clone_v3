#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def return_states():
    '''return lists of all states'''
    all_states = storage.all('State')
    new_list = [val.to_dict() for key, val in all_states.items()]
    return jsonify(new_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def return_states_id(state_id):
    '''returns lists of states with coresponding id'''
    all_states = storage.all('State')
    try:
        the_id = 'State.' + state_id
        obj = all_states.get(the_id).to_dict()
        return jsonify(obj)
    except Exception:
        abort(404)


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_states_id(state_id):
    ''' deletes the state with a corresponding id'''
    try:
        all_states = storage.all('State')
        the_id = 'State.' + state_id
        obj = all_states.get(the_id)
        obj.delete()
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    '''posts a new state'''
    try:
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in request.json:
            return jsonify({'error': 'Missing name'}), 400
        new_state = request.get_json().get('name')
        new_obj = State(name=new_state)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id):
    ''' Updates a state'''
    try:
        the_obj = storage.get('State', state_id)
        if the_obj is None:
            abort(404)
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400
        new_attrs = request.get_json()

        dont_add = {'id', 'created_at', 'updated_at'}
        for key, value in new_attrs.items():
            if key not in dont_add:
                setattr(the_obj, key, value)
        the_obj.save()
        return jsonify(the_obj.to_dict()), 200
    except Exception:
        abort(404)
