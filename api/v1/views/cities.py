#!/usr/bin/python3
# noinspection PyInterpreter,PyInterpreter
"""
This is a module that implements a blueprint
this blueprint is a kind of modularization of
flask applications.
The only requirement is that you will then
import this package file in main then register the
blueprint (app_views) as shown below

app.register_blueprint(app_views)

You can also override its url_prefix like so
app.register_blueprint(app_views, url_prefix="/diff/url")
"""
from flask import jsonify, escape, Blueprint, abort, render_template, request
from jinja2 import TemplateNotFound
import os


from api.v1.views import app_views
from models import BaseModel, storage,\
    Amenity, City, Review, State, User, Place

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """ Function returns list of cities by states and
    displays/renders them in a html document.
    when no get parameter is provided it will list all available
    states.
    When a state_id is provided it will list all cities within than state
    When a non_existent state_id is provided (url/states/<invalid_state_id>
    the page displays "Not found!"
    """
    temp = list()

    if True:
        if STORAGE_TYPE == "db":
            cities = storage.state_cities(state_id).values()
        else:
            cities = storage.all(City).values()

            # print(cities)

        for val in cities:
            temp.append(val.to_dict())
        if len(temp) < 1:
            abort(404)
        else:
            return jsonify(temp)


@app_views.route('cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """ Function returns list of cities by states and
    displays/renders them in a html document.
    when no get parameter is provided it will list all available
    states.
    When a state_id is provided it will list all cities within than state
    When a non_existent state_id is provided (url/states/<invalid_state_id>
    the page displays "Not found!"
    """
    temp = list()

    if True:
        if STORAGE_TYPE == "db":
            cities = storage.all("City").values()
        else:
            cities = storage.all(City).values()

            # print(cities)

        for val in cities:
            if val.id == city_id:
                temp.append(val.to_dict())
                break
        if len(temp) < 1:
            abort(404)
        else:
            return jsonify(temp)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def del_city(city_id):
    """ Function returns list of cities by states and
    displays/renders them in a html document.
    when no get parameter is provided it will list all available
    states.
    When a state_id is provided it will list all cities within than state
    When a non_existent state_id is provided (url/states/<invalid_state_id>
    the page displays "Not found!"
    """
    if city_id:
        if STORAGE_TYPE == "db":
            del_obj = storage.get("City", escape(city_id))
        else:
            # Handles File Storage
            # storage.get return an object dictionary else None
            del_obj = storage.get(City, escape(city_id))
        if del_obj:
            # storage.delete returns true on success else false
            del_status = storage.delete(del_obj)
            if del_status:
                return jsonify({})
            else:
                abort(404)
        else:
            abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def post_city(state_id):
    """ Creates a new State and initializes it with a state name
    if requested dictionary is none output 'Not a JSON'
    if post data does not contain the key 'name' output 'Missing name'
    On success return a status of 201 else 400
    """
    if STORAGE_TYPE == "db":
        state_obj = storage.get("State", escape(state_id))
    else:
        # Handles File Storage
        # storage.get return an object dictionary else None
        state_obj = storage.get(State, escape(state_id))
    if state_obj is None:
        abort(404, 'Not found')

    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if req_json.get("name") is None:
        abort(400, 'Missing name')
    req_json["state_id"] = state_id
    new_object = City(**req_json)
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ Updates a city's values
    if requested dictionary is none output 'Not a JSON'
    if post data does not contain the key 'name' output 'Missing name'
    On success return a status of 201 else 400
    """
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if req_json.get("name") is None:
        abort(400, 'Missing name')
    status = storage.update(City, city_id, req_json)

    if status:
        return jsonify(status.to_dict())
    else:
        abort(404)