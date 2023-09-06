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
    name = db.Column(db.String, unique=True, nullable=False)
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


# Event listener to update TournamentResult after Result
# @event.listens_for(Result, 'after_insert')
# def result_after_insert(mapper, connection, target):
#     new_results = target
#     match = Match.query.get(new_results.match_id)
#     tournament_id = match.tournament_id
#     nested_transaction = db.session.begin_nested()
#     if new_results.player_2_id is not None:
#         player_1_object = Player.query.get(new_results.player_1_id)
#         player_2_object = Player.query.get(new_results.player_2_id)
#         tournament_result_objects = TournamentResult.query.filter_by(tournament_id=tournament_id).all()
#         player_1_result_object = [item for item in tournament_result_objects
#                                   if item.player_id == player_1_object.id]
#         player_2_result_object = [item for item in tournament_result_objects
#                                   if item.player_id == player_2_object.id]
#         if new_results.player_1_wins > new_results.player_2_wins:
#             player_1_result_object[0].points += 3
#             player_1_result_object[0].matches_won += 1
#             player_1_result_object[0].games_won += new_results.player_1_wins
#             player_1_result_object[0].games_drawn += new_results.draws
#             player_2_result_object[0].games_won += new_results.player_2_wins
#             player_2_result_object[0].games_drawn += new_results.draws
#         elif new_results.player_1_wins < new_results.player_2_wins:
#             player_2_result_object[0].points += 3
#             player_2_result_object[0].matches_won += 1
#             player_2_result_object[0].games_won += new_results.player_2_wins
#             player_2_result_object[0].games_drawn += new_results.draws
#             player_1_result_object[0].games_won += new_results.player_1_wins
#             player_1_result_object[0].games_drawn += new_results.draws
#         else:
#             player_1_result_object[0].points += 1
#             player_2_result_object[0].points += 1
#             player_1_result_object[0].matches_drawn += 1
#             player_2_result_object[0].matches_drawn += 1
#             player_1_result_object[0].games_won += new_results.player_1_wins
#             player_1_result_object[0].games_drawn += new_results.draws
#             player_2_result_object[0].games_won += new_results.player_2_wins
#             player_2_result_object[0].games_drawn += new_results.draws
#     else:
#         player_1_object = Player.query.get(new_results.player_1_id)
#         tournament_result_objects = TournamentResult.query.filter_by(tournament_id=tournament_id).all()
#         player_1_result_object = [item for item in tournament_result_objects if
#                                   item.player_id == player_1_object.id]
#         player_1_result_object[0].points += 3
#         player_1_result_object[0].matches_won += 1
#         player_1_result_object[0].games_won += new_results.player_1_wins
#     nested_transaction.commit()
#
#
# def process_new_results(new_results):
#     return
