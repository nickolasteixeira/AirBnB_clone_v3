#!/usr/bin/python3
'''App_views routes'''
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models import Review


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['GET'],
    strict_slashes=False)
def return_reviews(place_id):
    ''' returns all reviews with the corresponding place_id'''
    if storage.get('Place', place_id) is None:
        abort(404)
    all_reviews = storage.all('Review')
    new_reviews = []
    for key, value in all_reviews.items():
        if place_id == value.place_id:
            new_reviews.append(value.to_dict())
    return jsonify(new_reviews), 201


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def return_review(review_id):
    ''' returns a single review obj based on the reveiw id'''
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    '/reviews/<review_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_review(review_id):
    ''' deletes a review obj based on the review id'''
    try:
        review = storage.get('Review', review_id)
        if review is None:
            abort(404)
        review.delete()
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False)
def post_review(place_id):
    ''' posts a new review to the places based on place_id'''
    try:
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' not in request.json:
            return jsonify({'error': 'Missing user_id'}), 400
        if 'text' not in request.json:
            return jsonify({'error': 'Missing text'}), 400

        place_obj = storage.get('Place', place_id)
        if place_obj is None:
            abort(404)
        user_id = request.get_json().get('user_id')
        user_obj = storage.get('User', user_id)
        if user_obj is None:
            abort(404)

        text = request.get_json().get('text')
        new_obj = Review(text=text, place_id=place_id, user_id=user_id)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''updates a review based on the review id'''
    try:
        review = storage.get('Review', review_id)
        if review is None:
            abort(404)
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400

        new_attrs = request.get_json()
        dont_add = {'id', 'user_id', 'place_id', 'created_at', 'updated_at'}
        for key, value in new_attrs.items():
            if key not in dont_add:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    except Exception:
        abort(404)
