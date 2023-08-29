import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournaments.db'
db = SQLAlchemy(app)


# Player with tournament and their result
class PlayersAndTournaments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tournament = db.Column(db.String, unique=False, nullable=False)
    player = db.Column(db.String, unique=True, nullable=False)
    points = db.Column(db.Integer, nullable=True)
    matches_won = db.Column(db.Integer, nullable=True)
    matches_drawn = db.Column(db.Integer, nullable=True)
    games_won = db.Column(db.Integer, nullable=True)
    pmw = db.Column(db.Float, nullable=True)
    omw = db.Column(db.Float, nullable=True)
    pgw = db.Column(db.Float, nullable=True)
    ogw = db.Column(db.Float, nullable=True)


# Tournament with data for each one
class Tournaments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    winner = db.Column(db.String, unique=False, nullable=False)
    n_players = db.Column(db.Integer, unique=False, nullable=False)
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
    player1_match_wins = db.Column(db.Integer, unique=False, nullable=True)
    player1_game_wins = db.Column(db.Integer, unique=False, nullable=True)
    player2_match_wins = db.Column(db.Integer, unique=False, nullable=True)
    player2_game_wins = db.Column(db.Integer, unique=False, nullable=True)


app.app_context().push()
db.create_all()


@app.route('/')
def home():
    # Just placeholder code for home which shouldn't require anything specific at the moment
    response_data = {'message': 'Home Page loaded successfully.'}
    return jsonify(response_data), 200


# Create empty tournament tables with custom name and add players to it
@app.route('/players', methods=['POST'])
def create_tournament():
    try:
        tournament = json.loads(request.get_json())
        tournament_name = tournament['name']
        player_names = tournament['players']
        for player_name in player_names:
            player = PlayersAndTournaments(
                tournament=tournament_name,
                player=player_name
            )
            db.session.add(player)
        db.session.commit()
        response_data = {'message': 'Data received successfully.'}
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


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


# Probably another huge pile of garbage
# Add a list of players to existing tournament table
# Currently to be deprecated
@app.route('/players/add', methods=['POST'])
def add_player():
    try:
        data = json.loads(request.get_json())
        tournament_name = data['tournament']
        player_names = data['players']
        for player_name in player_names:
            player = tournament_name(
                player=player_name
            )
            db.session.add(player)
            db.session.commit()
        response_data = {'message': 'Data received successfully'}
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
