from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, event
from pprint import pprint


db = SQLAlchemy()

players_and_tournaments = db.Table('players_and_tournaments',
                                   db.Column('player_id', db.Integer, ForeignKey('player.id')),
                                   db.Column('tournament_id', db.Integer, ForeignKey('tournament.id')))

players_match_association = db.Table('players_match_association',
                                     db.Column('player_id', db.Integer, ForeignKey('player.id')),
                                     db.Column('match_id', db.Integer, ForeignKey('match.id')))


class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=False, nullable=False)
    # defining relationships
    tournaments = db.relationship('Tournament', secondary=players_and_tournaments, back_populates='players')
    matches = db.relationship('Match', secondary=players_match_association, back_populates='players')
    tournaments_results = db.relationship('TournamentResult', backref='player')


# Tournament with data for each one
class Tournament(db.Model):
    __tablename__ = 'tournament'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    date = db.Column(db.String, unique=False, nullable=False)
    # defining relationships
    players = db.relationship('Player', secondary=players_and_tournaments, back_populates='tournaments')
    rounds = db.relationship('Match', backref='tournament')
    tournament_result = db.relationship('TournamentResult', backref='tournament')


# Match of each tournament
class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tournament_id = db.Column(db.Integer, ForeignKey('tournament.id'), nullable=False)
    round_number = db.Column(db.Integer, unique=False, nullable=False)
    table_number = db.Column(db.Integer, unique=False, nullable=False)
    # defining relationships
    players = db.relationship('Player', secondary=players_match_association, back_populates='matches')
    result = db.relationship('Result', backref='match', uselist=False)


# Result of each match
class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_id = db.Column(db.Integer, ForeignKey('match.id'), nullable=False)
    player_1_id = db.Column(db.Integer, ForeignKey('player.id'), nullable=True)
    player_2_id = db.Column(db.Integer, ForeignKey('player.id'), nullable=True)
    player_1_wins = db.Column(db.Integer, unique=False, nullable=False)
    player_2_wins = db.Column(db.Integer, unique=False, nullable=False)
    draws = db.Column(db.Integer, unique=False, nullable=False)
    date = db.Column(db.String, unique=False, nullable=True)
    time = db.Column(db.String, unique=False, nullable=True)
    # defining relationships
    player_1 = db.relationship('Player', foreign_keys=[player_1_id])
    player_2 = db.relationship('Player', foreign_keys=[player_2_id])


# Player with tournament and their result
class TournamentResult(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tournament_id = db.Column(db.Integer, ForeignKey('tournament.id'), nullable=False)
    player_id = db.Column(db.Integer, ForeignKey('player.id'), nullable=False)
    points = db.Column(db.Integer, unique=False, nullable=True)
    matches_won = db.Column(db.Integer, unique=False, nullable=True)
    matches_drawn = db.Column(db.Integer, unique=False, nullable=True)
    games_won = db.Column(db.Integer, unique=False, nullable=True)
    games_drawn = db.Column(db.Integer, unique=False, nullable=True)
