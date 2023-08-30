import json
import flask_functions
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournaments.db'
db = SQLAlchemy(app)


class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=False, nullable=False)


# Tournament with data for each one
class Tournaments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    date = db.Column(db.String, unique=False, nullable=False)


# Rounds of each tournament (probably not even need, maybe)
class Rounds(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tournament = db.Column(db.String, unique=False, nullable=False)
    round_number = db.Column(db.Integer, unique=False, nullable=False)
    player1 = db.Column(db.String, unique=False, nullable=False)
    player2 = db.Column(db.String, unique=False, nullable=False)
    player1_result = db.Column(db.Integer, unique=False, nullable=False)
    player2_result = db.Column(db.Integer, unique=False, nullable=False)


# Player with tournament and their result
class PlayersAndTournaments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tournament = db.Column(db.String, unique=False, nullable=False)
    player = db.Column(db.String, unique=True, nullable=False)
    points = db.Column(db.Integer, nullable=True)
    matches_won = db.Column(db.Integer, nullable=True)
    matches_drawn = db.Column(db.Integer, nullable=True)
    games_won = db.Column(db.Integer, nullable=True)


app.app_context().push()
db.create_all()


@app.route('/')
def home():
    # Just placeholder code for home which shouldn't require anything specific at the moment
    response_data = {'message': 'Home Page loaded successfully.'}
    return jsonify(response_data), 200


# Populate PlayersAndTournament at the tournament start (url to be updated)
@app.route('/tournaments/start', methods=['POST'])
def start_tournament():
    try:
        response_data = flask_functions.add_players_to_tournament_db(db=db, db_table=PlayersAndTournaments)
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Create tournament row in the tournament db table
@app.route('/tournaments', methods=['POST'])
def create_tournaments():
    try:
        response_data = flask_functions.create_tournament(db=db, db_table=Tournaments)
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Save player into the player db table
@app.route('/players/add', methods=['POST'])
def add_players():
    try:
        response_data = flask_functions.add_players_to_db(db=db, db_table=Players)
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Save round result into round db table
@app.route('/rounds', methods=['POST'])
def add_rounds():
    try:
        response_data = flask_functions.add_rounds_to_db(db=db, db_table=Rounds)
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Probably a pile of garbage
@app.route('/delete_tournament', methods=['DELETE'])
def delete_tournament():
    try:
        tournament = json.loads(request.get_json())
        tournament_name = tournament['name']
        db.session(f'DROP TABLE {tournament_name}')
        db.session.commit()
        response_data = {'message': f'{tournament_name} table deleted'}
        return jsonify(response_data), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
