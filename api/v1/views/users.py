#!/usr/bin/python3
'''App_views routes'''
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models import User


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def return_user(user_id):
    '''return user corresponding to user_id'''
    the_user = storage.get('User', user_id)
    if the_user is None:
        abort(404)
    return jsonify(the_user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    ''' deletes the user corresponding to the user_id'''
    try:
        the_user = storage.get('User', user_id)
        if the_user is None:
            abort(404)
        the_user.delete()
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    ''' create a new user'''
    try:
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400
        new_attrs = request.get_json()
        if 'email' not in new_attrs:
            return jsonify({'error': 'Missing email'}), 400
        if 'password' not in new_attrs:
            return jsonify({'error': 'Missing password'}), 400

        email = request.get_json().get('email')
        password = request.get_json().get('password')
        new_obj = User(email=email, password=password)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201
    except Exception:
        abort(404)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    ''' updates the user based on user id'''
    try:
        the_obj = storage.get('User', user_id)
        if the_obj is None:
            abort(404)
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400

        new_attrs = request.get_json()
        dont_add = {'id', 'created_at', 'udpated_at'}
        for key, value in new_attrs.items():
            if key not in dont_add:
                setattr(the_obj, key, value)
        the_obj.save()
        return jsonify(the_obj.to_dict()), 200
    except Exception:
        abort(404)
