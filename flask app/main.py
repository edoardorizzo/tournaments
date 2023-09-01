import flask_functions
from flask import Flask, jsonify
from models import Player, Tournament, Match, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournaments.db'

db.init_app(app)
app.app_context().push()
db.create_all()


@app.route('/')
def home():
    # Just placeholder code for home which shouldn't require anything specific at the moment
    response_data = {'message': 'Home Page loaded successfully.'}
    return jsonify(response_data), 200


# Create tournament row in the tournament db table
@app.route('/tournaments/start_new', methods=['POST'])
def start_tournament():
    try:
        response_data = flask_functions.start_tournament(db=db, tournament_table=Tournament, player_table=Player)
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Get list of saved players
@app.route('/players/saved', methods=['GET'])
def saved_players():
    try:
        players = flask_functions.get_saved_players(db_table=Player)
        return jsonify(players)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# The following routes are not yet implemented or actually useful


# Save player into the player db table
@app.route('/players/add', methods=['POST'])
def add_players():
    try:
        response_data = flask_functions.add_players_to_db(db=db, db_table=Player)
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Save round result into round db table
@app.route('/rounds', methods=['POST'])
def add_rounds():
    try:
        response_data = flask_functions.add_rounds_to_db(db=db, db_table=Match)
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Get tournament current results
@app.route('/tournaments/<int:tournament_id>', methods=['GET'])
def get_tournament_name_and_players(tournament_id):
    request_tournament = Tournament.query.get(tournament_id)
    if request_tournament:
        players = request_tournament.players
        return jsonify({'tournament': request_tournament,
                        'players': players}), 200
    else:
        return jsonify({'error': 'tournament not found'}), 404


# Populate PlayersAndTournament at the tournament start (url to be updated)
# @app.route('/tournaments/start', methods=['POST'])
# def start_tournament():
#     try:
#         response_data = flask_functions.add_players_to_tournament_db(db=db, db_table=PlayersAndTournaments)
#         return jsonify(response_data), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
