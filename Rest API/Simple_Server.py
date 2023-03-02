from flask import Flask, request, render_template, abort, make_response, jsonify, Response
import json
import os

app = Flask(__name__)

stuff = [
    {
        "id": 1,
        "name": "Guitar",
        "description": "Six - string"
    },
    {
        "id": 2,
        "name": "Drum",
        "description": "Percussion instrument"
    },
    {
        "id": 3,
        "name": "Microphone",
        "description": "Very loudly"
    },
    {
        'id': 4,
        'name': "Saxophone",
        "description": "So jazzy"
    },
    {
        "id": 5,
        "name": "Piano",
        "description": "Melodic"
    },
    {
        "id": 6,
        "name": "Contrabass",
        "description": "Cool bass"
    },
    {
        'id': 7,
        'name': "Trumpet",
        "description": "Brass section"
    },
    {
        "id": 8,
        "name": "Banjo",
        "description": "Dance-tunes"
    },
    {
        "id": 9,
        "name": "Trombone",
        "description": "Another brass section"
    },
    {
        "id": 10,
        "name": "Clarinet",
        "description": "Conservatoire"
    }
]


@app.route('/')
def home():
    return "App Works!"


@app.route('/get_stuff', methods=["GET"])  # Get all product list
def stuff():
    return json.dumps(stuff, indent=3)


@app.route('/get_stuff/<int:stuff_id>', methods=['GET'])  # GET for only one id
def get_ont_stuff(stuff_id):
    one_stuff = filter(lambda one: one['id'] == stuff_id, stuff)
    if len(one_stuff['id']) == 0:
        abort(404)
    return json.dumps(one_stuff[0])


@app.route('/post_stuff', methods=['POST'])  # POST new product
def create_stuff():
    if not (request.json or 'name' in request.json):
        abort(400)
    one_stuff = {
        'id': stuff[-1]['id'] + 1,
        'name': request.json['name'],
        'description': request.json.get('description', ""),
    }
    stuff.append(one_stuff)
    return json.dumps(stuff), 201


@app.route('/put_stuff/<int:stuff_id>', methods=['PUT'])  # PUT change data
def update_task(stuff_id):
    one_stuff = filter(lambda t: t['id'] == stuff_id, stuff)
    if len(one_stuff['id']) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    one_stuff[0]['name'] = request.json.get('title', one_stuff[0]['name'])
    one_stuff[0]['description'] = request.json.get('description', one_stuff[0]['description'])
    return json.dumps(one_stuff[0])


@app.route('/del_stuff/<int:stuff_id>', methods=['DELETE'])  # DELETE data
def delete_task(stuff_id):
    one_stuff = filter(lambda t: t['id'] == stuff_id, stuff)
    if len(one_stuff['id']) == 0:
        abort(404)
    stuff.remove(one_stuff[0])
    return json.dumps(True)


if __name__ == "__main__":
    app.run(debug=False)
