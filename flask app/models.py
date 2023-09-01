from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey


db = SQLAlchemy()

players_and_tournaments = db.Table('players_and_tournaments',
                                   db.Column('player_id', db.Integer, ForeignKey('player.id')),
                                   db.Column('tournament_id', db.Integer, ForeignKey('tournament.id')))


class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=False, nullable=False)
    tournaments = db.relationship('Tournament', secondary=players_and_tournaments, back_populates='players')
    matches = db.relationship('Match', backref='player')


# Tournament with data for each one
class Tournament(db.Model):
    __tablename__ = 'tournament'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    date = db.Column(db.String, unique=False, nullable=False)
    players = db.relationship('Player', secondary=players_and_tournaments, back_populates='tournaments')
    rounds = db.relationship('Match', backref='tournament')


# Rounds of each tournament (probably not even need, maybe)
class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    round_number = db.Column(db.Integer, unique=False, nullable=False)
    players = db.Column(db.Integer, ForeignKey('player.id'), nullable=True)
    # player2 = db.Column(db.Integer, ForeignKey('player.id'), nullable=True)
    player1_result = db.Column(db.Integer, unique=False, nullable=False)
    player2_result = db.Column(db.Integer, unique=False, nullable=False)
    tournament_id = db.Column(db.Integer, ForeignKey('tournament.id'), nullable=False)


# Player with tournament and their result
# Currently it's kinda a mess
# class PlayersAndTournaments(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     tournament = db.Column(db.String, unique=False, nullable=False)
#     player = db.Column(db.String, unique=False, nullable=False)
#     points = db.Column(db.Integer, unique=False, nullable=True)
#     matches_won = db.Column(db.Integer, unique=False, nullable=True)
#     matches_drawn = db.Column(db.Integer, unique=False, nullable=True)
#     games_won = db.Column(db.Integer, unique=False, nullable=True)
