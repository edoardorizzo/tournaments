from flask import request
from flask_sqlalchemy import SQLAlchemy
import swiss_manager

sqlalchemy = SQLAlchemy()


# Function for start_tournament()
def start_tournament(db: sqlalchemy, tournament_table: sqlalchemy.Model, player_table: sqlalchemy.Model) -> dict:
    """
    Gets input from request's json. Checks if the tournament exists, creates it if it doesn't.
    Appends players to tournament many-to-many relationship and returns response data to be turned into json.
    """
    request_data = request.get_json()
    check_tournament_existence = tournament_table.query.filter_by(name=request_data['tournament']).first()
    if check_tournament_existence:
        tournament_query = tournament_table.query.filter_by(name=request_data['tournament'])
        tournament = tournament_query.first()
    else:
        tournament = tournament_table(
            name=request_data['tournament'],
            date=request_data['date']
        )
        db.session.add(tournament)
        db.session.commit()
    players = request_data['players']
    for player in players:
        query_for_player = player_table.query.filter_by(name=player)
        player_row = query_for_player.first()
        player_row.tournaments.append(tournament)
    db.session.commit()
    player_names = []
    for player in tournament.players:
        player_names.append(player.name)
    response_data = {
        'id': tournament.id,
        'name': tournament.name,
        'date': tournament.date,
        'players': player_names
    }
    return response_data


# Function to get saved players
def get_saved_players(model: sqlalchemy.Model) -> list:
    """
    Returns a list of dictionaries containing player id and player name
    """
    players_objects = model.query.all()
    players = []
    if len(players_objects) > 0:
        for player in players_objects:
            player_dict = {'id': player.id, 'name': player.name}
            players.append(player_dict)
    return players


# Function to get saved tournaments
def get_saved_tournaments(model: sqlalchemy.Model) -> list:
    """
    Returns a list of dictionaries containing tournament id, tournament name and tournament date
    """
    tournaments_objects = model.query.all()
    tournaments = []
    if len(tournaments_objects) > 0:
        for tournament in tournaments_objects:
            tournament_dict = {'id': tournament.id, 'name': tournament.name, 'date': tournament.date}
            tournaments.append(tournament_dict)
    return tournaments


# Function for add_players()
def add_players_to_db(db: sqlalchemy, model: sqlalchemy.Model) -> list:
    """
    Saves a players list from request into the player db table
    """
    player_data = request.get_json()
    response_data = []
    for player_name in player_data:
        player = model(
            name=player_name
        )
        db.session.add(player)
        db.session.commit()
        player_response = {
            'id': player.id,
            'name': player.name
        }
        response_data.append(player_response)
    return response_data


# Function for first_round()
def create_first_round(db, tournament_table: sqlalchemy.Model, match_table: sqlalchemy.Model,
                       player_table: sqlalchemy.Model, tournament_id: int) -> list:
    """
    Gets a tournament by its id and creates the first round from players registered in the tournament
    """
    players = get_players_in_tournament(tournament_table=tournament_table, tournament_id=tournament_id)
    pairings = swiss_manager.first_round_pairings(player_list=players)
    response_data = []
    for i in range(len(pairings)):
        match = match_table(
            tournament_id=tournament_id,
            round_number=1,
            table_number=i+1
        )
        db.session.add(match)
        for player in pairings[i]:
            if player != "Bye":
                query_for_player = player_table.query.filter_by(name=player)
                player_object = query_for_player.first()
                match.players.append(player_object)
        match_data = {
            'match_id': match.id,
            'round': 1,
            'table_number': i + 1,
            'player_1': pairings[i][0],
            'player_2': pairings[i][1]
        }
        response_data.append(match_data)
    db.session.commit()
    return response_data


# Function for tournament_players()
def get_players_in_tournament(tournament_table: sqlalchemy.Model, tournament_id: int) -> list:
    """
    Returns a list of players registered into a given tournament
    """
    tournament = tournament_table.query.get(tournament_id)
    player_objects = tournament.players
    players = []
    for player_object in player_objects:
        player = player_object.name
        players.append(player)
    return players


# Function for post_results()
def save_round_results(db, tournament_id: int, round_number: int, result_table: sqlalchemy.Model):
    round_data = request.get_json()
    for match in round_data:
        match_data = result_table(
            match_id=match['match_id'],
            player_1=match['player_1'],
            player_2=match['player_2'],
            player_1_wins=match['player_1_wins'],
            player_2_wins=match['player_2_wins'],
            draws=match['draws']
        )
        db.session.add(match_data)
        # TODO: update values in TournamentResult table with if condition to check result
        # TODO: create the response data
    request_data = [
        {
            'match_id': 1,
            'player_1': "bla",
            'player_2': "blabla",
            'player_1_wins': 2,
            'player_2_wins': 1,
            'draws': 0
        }
    ]


# # # - - - # # # - - - # # # - - - # # # - - - # # # - - - # # # - - - # # # - - - # # # - - - #
# All the following functions are working but not actually implemented into the app for now - - #
# # # - - - # # # - - - # # # - - - # # # - - - # # # - - - # # # - - - # # # - - - # # # - - - #

def add_players_to_tournament_db(db, model):
    tournament = request.get_json()
    player_names = tournament['player_names']
    response_data = []
    for player_name in player_names:
        player = model(
            tournament=tournament['tournament'],
            player=player_name
        )
        db.session.add(player)
        db.session.commit()
        player_response = {
            'id': player.id,
            'tournament': player.tournament,
            'players': player.player
        }
        response_data.append(player_response)
    return response_data


# Function for create_tournaments()
def create_tournament(db, model):
    tournament_data = request.get_json()
    tournament = model(
        name=tournament_data['name'],
        date=tournament_data['date']
    )
    db.session.add(tournament)
    db.session.commit()
    response_data = {
        'id': tournament.id,
        'name': tournament.name,
        'date': tournament.date
    }
    return response_data


# Function for add_rounds()
def add_rounds_to_db(db, model):
    round_data = request.get_json()
    response_data = []
    for round_match in round_data:
        match = model(
            tournament=round_match['tournament'],
            round_number=round_match['round_number'],
            player1=round_match['player1'],
            player2=round_match['player2'],
            player1_result=round_match['player1_result'],
            player2_result=round_match['player2_result']
        )
        db.session.add(match)
        resp_data = {
            # this way the id here is Null, better move this outside this for loop
            'id': match.id,
            'tournament': match.tournament,
            'round_number': match.round_number,
            'player1': match.player1,
            'player2': match.player2,
            'player1_result': match.player1_result,
            'player2_result': match.player2_result
        }
        response_data.append(resp_data)
    db.session.commit()
    return response_data
