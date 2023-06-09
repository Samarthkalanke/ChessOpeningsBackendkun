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
    def get_games():
        with open('games.json') as f:
            games_data = json.load(f)
        return games_data

    @staticmethod
    def write_games(games_data):
        with open('games.json', 'w') as f:
            json.dump(games_data, f, indent=4)

    class _Create(Resource):
        def post(self):
            body = request.get_json()
            name = body.get("name")
            score = int(body.get("score"))

            # Validate name
            if name is None or len(name) < 2:
                return {'message': 'Name is missing or less than 2 characters'}, 210

            # Validate score
            if score is None or score < 0:
                return {'message': 'Score is missing or not a valid value'}, 210

            games_data = ChessAPI.get_games()

            # Check if the game with the given name already exists
            existing_game = next((game for game in games_data if game["name"] == name), None)
            if existing_game:
                return {'message': f'Game with name {name} already exists'}, 210

            new_game = {"name": name, "score": score}
            games_data.append(new_game)

            ChessAPI.write_games(games_data)

            return jsonify(games_data)

    class _Read(Resource):
        def get(self):
            games_data = ChessAPI.get_games()
            return jsonify(games_data)

    class _Update(Resource):
        def put(self):
            body = request.get_json()
            name = body.get("name")
            new_score = int(body.get("score"))

            games_data = ChessAPI.get_games()

            # Find the game with the given name
            game = next((game for game in games_data if game["name"] == name), None)
            if game:
                game["score"] = new_score
                ChessAPI.write_games(games_data)
                return jsonify(game)
            else:
                return {'message': f'Game with name {name} not found'}, 210

    class _Delete(Resource):
        def delete(self, name):
            games_data = ChessAPI.get_games()

            # Find the game with the given name
            game = next((game for game in games_data if game["name"] == name), None)
            if game:
                games_data.remove(game)
                ChessAPI.write_games(games_data)
                return {'message': f'Successfully deleted game with name {name}'}
            else:
                return {'message': f'Game with name {name} not found'}, 210

# Building REST API endpoints
api.add_resource(ChessAPI._Create, '/create')
api.add_resource(ChessAPI._Read, '/')
api.add_resource(ChessAPI._Update, '/update')
api.add_resource(ChessAPI._Delete, '/delete/<string:name>')