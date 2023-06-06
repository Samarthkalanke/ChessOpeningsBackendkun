from contextlib import nullcontext
from flask import Blueprint, json, jsonify, request  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import requests  # used for testing 
import time
from flask_restful import Resource

chess_api = Blueprint('chess_api', __name__,
                      url_prefix='/api/chess')
api = Api(chess_api)


class ChessAPI:
    @staticmethod
    def get_chess():
        with open('chess.json') as f:
            chess_data = json.load(f)
        return chess_data

    @staticmethod
    def write_chess(chess_data):
        with open('chess.json', 'w') as f:
            json.dump(chess_data, f, indent=4)

    class _Create(Resource):
        def post(self):
            body = request.get_json()
            name = body.get("name")
            score = int(body.get("score"))  # Extract score and convert it to integer

            # Validate name
            if name is None or len(name) < 2:
                return {'message': f'Name is missing or less than 2 characters'}, 210

            # Validate score
            if score is None or score < 0:  # Assuming score cannot be negative
                return {'message': f'Score is missing or not a valid value'}, 210

            chess_data = ChessAPI.get_chess()

            # Check if the film with the given name already exists
            existing_film = next((film for film in chess_data if film["name"] == name), None)
            if existing_film:
                return {'message': f'Film with name {name} already exists'}, 210

            new_film = {"name": name, "score": score}
            chess_data.append(new_film)

            ChessAPI.write_chess(chess_data)

            return jsonify(new_film)

    class _Read(Resource):
        def get(self):
            chess_data = ChessAPI.get_chess()
            return jsonify(chess_data)

    class _Update(Resource):
        def put(self):
            body = request.get_json()
            name = body.get("name")
            score = int(body.get("score"))  # Extract score and convert it to integer

            # Validate name
            if name is None or len(name) < 2:
                return {'message': f'Name is missing or less than 2 characters'}, 210

            # Validate score
            if score is None or score < 0:  # Assuming score cannot be negative
                return {'message': f'Score is missing or not a valid value'}, 210

            chess_data = ChessAPI.get_chess()

            # Find the film with the given name
            film = next((film for film in chess_data if film["name"] == name), None)
            if film:
                film["score"] = score
                ChessAPI.write_chess(chess_data)
                return {'message': f'Successfully updated score for film: {name}'}

            return {'message': f'Film with name {name} not found'}, 210

    class _Delete(Resource):
        def delete(self, name):
            if name == '-':
                chess_data = []
                ChessAPI.write_chess(chess_data)
                return {'message': f'Successfully deleted all chess'}
            else:
                chess_data = ChessAPI.get_chess()

                # Find the film with the given name
                film = next((film for film in chess_data if film["name"] == name), None)
                if film:
                    chess_data.remove(film)
                    ChessAPI.write_chess(chess_data)
                    return {'message': f'Successfully deleted film: {name}'}

                return {'message': f'Film with name {name} not found'}, 210

    # Building REST API endpoints
    chess_api.add_resource(_Create, '/create')
    chess_api.add_resource(_Read, '/')
    chess_api.add_resource(_Update, '/update')
    chess_api.add_resource(_Delete, '/delete/<string:name>')