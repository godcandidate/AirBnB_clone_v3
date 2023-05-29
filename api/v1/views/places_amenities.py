#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from os import environ

STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_per_place(place_id=None):
    place_obj = storage.get('Place', place_id)

    if place_obj is None:
        abort(404)

    if request.method == 'GET':
        amenities = []
        if STORAGE_TYPE == 'db':
            amenities = place_obj.amenities
        else:
            amenity_ids = place_obj.amenity_ids
            amenities = [storage.get('Amenity',
                                     amenity_id) for amenity_id in amenity_ids]
        amenities = [amenity.to_dict() for amenity in amenities]
        return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def manage_amenity_to_place(place_id=None, amenity_id=None):
    place_obj = storage.get('Place', place_id)
    amenity_obj = storage.get('Amenity', amenity_id)

    if place_obj is None or amenity_obj is None:
        abort(404)

    if request.method == 'DELETE':
        if amenity_obj not in place_obj.amenities:
            abort(404)
        place_obj.amenities.remove(amenity_obj)
        place_obj.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if amenity_obj in place_obj.amenities:
            return jsonify(amenity_obj.to_dict()), 200
        place_obj.amenities.append(amenity_obj)
        place_obj.save()
        return jsonify(amenity_obj.to_dict()), 201
