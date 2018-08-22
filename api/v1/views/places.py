#!/usr/bin/python3
"""
Places Api Module
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_CityId(city_id):
    """
    Return All Places by City
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    """
    Return Place by id
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return(jsonify(place.to_dict()))


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_id(place_id):
    """
    Deletes a Place by id
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    else:
        storage.delete(storage.get('Place', place_id))
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<string:city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """
    Create Place In City
    """
    if storage.get("City", city_id) is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    places_dict = request.get_json()
    if "user_id" not in places_dict:
        return jsonify({"error": "Missing user_id"}), 400
    if storage.get("User", places_dict["user_id"]) is None:
        abort(404)
    if "name" not in places_dict:
        return jsonify({"error": "Missing name"}), 400
    else:
        place_usr_id = places_dict["user_id"]
        place_name = places_dict["name"]
        place = Place(user_id=place_usr_id, name=place_name, city_id=city_id)
        for key, value in places_dict.items():
            setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<string:place_id>", methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id):
    """
    Update Place obj by id
    """
    place = storage.get("Place", place_id)
    info_fields = ["id", "city_id", "user_id", "created_at", "updated_at"]
    if not place:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    response = request.get_json()
    for key, value in response.items():
        if key not in info_fields:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
