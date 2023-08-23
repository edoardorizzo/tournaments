import json
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournaments.db'
db = SQLAlchemy(app)


def create_tournament_table_class(table_name: str):
    class TournamentTable(db.Model):
        sql_table_name = table_name.lower().replace(' ', '_')
        __tablename__ = sql_table_name
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        player = db.Column(db.String, unique=True, nullable=False)
        points = db.Column(db.Integer, nullable=True)
        matches_won = db.Column(db.Integer, nullable=True)
        matches_drawn = db.Column(db.Integer, nullable=True)
        games_won = db.Column(db.Integer, nullable=True)
    return TournamentTable


app.app_context().push()
db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/tournaments', methods=['POST'])
def create_tournament():
    try:
        tournament = json.loads(request.get_json())
        tournament_name = tournament['name']
        create_tournament_table_class(table_name=tournament_name)
        db.create_all()
        response_data = {'message': 'Data received successfully.'}
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/players', methods=['GET', 'POST'])
def add_player():
    try:
        data = json.loads(request.get_json())
        tournament_name = data['tournament']['name']
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
