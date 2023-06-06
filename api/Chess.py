from flask import Blueprint, request, jsonify
import json

film_api = Blueprint('film_api', __name__, url_prefix='/api/films')


class FilmAPI:
    @staticmethod
    def get_films():
        with open('films.json') as f:
            films_data = json.load(f)
        return films_data

    @staticmethod
    def write_films(films_data):
        with open('films.json', 'w') as f:
            json.dump(films_data, f, indent=4)

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

            films_data = FilmAPI.get_films()

            # Check if the film with the given name already exists
            existing_film = next((film for film in films_data if film["name"] == name), None)
            if existing_film:
                return {'message': f'Film with name {name} already exists'}, 210

            new_film = {"name": name, "score": score}
            films_data.append(new_film)

            FilmAPI.write_films(films_data)

            return jsonify(new_film)

    class _Read(Resource):
        def get(self):
            films_data = FilmAPI.get_films()
            return jsonify(films_data)

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

            films_data = FilmAPI.get_films()

            # Find the film with the given name
            film = next((film for film in films_data if film["name"] == name), None)
            if film:
                film["score"] = score
                FilmAPI.write_films(films_data)
                return {'message': f'Successfully updated score for film: {name}'}

            return {'message': f'Film with name {name} not found'}, 210

    class _Delete(Resource):
        def delete(self, name):
            if name == '-':
                films_data = []
                FilmAPI.write_films(films_data)
                return {'message': f'Successfully deleted all films'}
            else:
                films_data = FilmAPI.get_films()

                # Find the film with the given name
                film = next((film for film in films_data if film["name"] == name), None)
                if film:
                    films_data.remove(film)
                    FilmAPI.write_films(films_data)
                    return {'message': f'Successfully deleted film: {name}'}

                return {'message': f'Film with name {name} not found'}, 210

    # Building REST API endpoints
    film_api.add_resource(_Create, '/create')
    film_api.add_resource(_Read, '/')
    film_api.add_resource(_Update, '/update')
    film_api.add_resource(_Delete, '/delete/<string:name>')
