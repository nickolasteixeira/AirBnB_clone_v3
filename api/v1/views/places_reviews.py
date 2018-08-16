#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models import Review
''' App_views routes'''


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['GET'],
    strict_slashes=False)
def return_reviews(place_id):
    ''' returns all reviews with the corresponding place_id'''
    all_reviews = storage.all('Review')
    new_reviews = []
    for key, value in all_reviews.items():
        obj = value.to_dict()
        if place_id == obj.get('place_id'):
            new_reviews.append(obj)

    if len(new_reviews) == 0:
        abort(404)
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
        user_obj = storage.get('User', request.get_json().get('user_id'))
        if user_ojb is None:
            abort(404)

        new_obj = Review(text=text, place_id=place_id, user_id=user_id)
        storage.save()
        return jsonify(new_obj.to_dict()), 201
    except Exception:
        abort(404)