from flask import request
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
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
def create_first_round(db: sqlalchemy, tournament_table: sqlalchemy.Model, match_table: sqlalchemy.Model,
                       player_table: sqlalchemy.Model, tournament_result_table: sqlalchemy.Model,
                       tournament_id: int) -> list:
    """
    Gets a tournament by its id and creates the first round from players registered in the tournament
    """
    players = get_players_in_tournament(tournament_table=tournament_table, tournament_id=tournament_id)
    create_tournament_result_rows(db=db, tournament_id=tournament_id,
                                  tournament_result_table=tournament_result_table, player_table=player_table,
                                  player_list=players)
    pairings = swiss_manager.first_round_pairings(player_list=players)
    response_data = []
    for i in range(len(pairings)):
        match = match_table(
            tournament_id=tournament_id,
            round_number=1,
            table_number=i + 1
        )
        db.session.add(match)
        for player in pairings[i]:
            if player != "Bye":
                player_object = player_table.query.get(player['id'])
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
        player = {'name': player_object.name, 'id': player_object.id}
        players.append(player)
    return players


# Function for post_results()
def save_round_results(db: sqlalchemy, tournament_id: int, player_table: sqlalchemy.Model,
                       result_table: sqlalchemy.Model, tournament_result_table: sqlalchemy.Model) -> list:
    """
    Saves matches results into the Result table and updates the TournamentResult rows
    """
    round_data = request.get_json()
    tournament_result_objects = tournament_result_table.query.filter_by(tournament_id=tournament_id).all()
    for match in round_data:
        match_data = result_table(
            match_id=match['match_id'],
            player_1_id=match['player_1']['id'],
            player_2_id=match['player_2']['id'],
            player_1_wins=match['player_1']['wins'],
            player_2_wins=match['player_2']['wins'],
            draws=match['player_1']['draws']
        )
        db.session.add(match_data)
        # TODO move this block of horrible code to a different module
        if match['player_2']['id'] is not None:
            player_1_object = player_table.query.get(match['player_1']['id'])
            player_2_object = player_table.query.get(match['player_2']['id'])
            player_1_result_object = [item for item in tournament_result_objects
                                      if item.player_id == player_1_object.id]
            player_2_result_object = [item for item in tournament_result_objects
                                      if item.player_id == player_2_object.id]
            if match['player_1']['wins'] > match['player_2']['wins']:
                player_1_result_object[0].points += 3
                player_1_result_object[0].matches_won += 1
                player_1_result_object[0].games_won += match['player_1']['wins']
                player_1_result_object[0].games_drawn += match['player_1']['draws']
                player_2_result_object[0].games_won += match['player_2']['wins']
                player_2_result_object[0].games_drawn += match['player_1']['draws']
            elif match['player_1']['wins'] < match['player_2']['wins']:
                player_2_result_object[0].points += 3
                player_2_result_object[0].matches_won += 1
                player_2_result_object[0].games_won += match['player_2']['wins']
                player_2_result_object[0].games_drawn += match['player_1']['draws']
                player_1_result_object[0].games_won += match['player_1']['wins']
                player_1_result_object[0].games_drawn += match['player_1']['draws']
            else:
                player_1_result_object[0].points += 1
                player_2_result_object[0].points += 1
                player_1_result_object[0].matches_drawn += 1
                player_2_result_object[0].matches_drawn += 1
                player_1_result_object[0].games_won += match['player_1']['wins']
                player_1_result_object[0].games_drawn += match['player_1']['draws']
                player_2_result_object[0].games_won += match['player_2']['wins']
                player_2_result_object[0].games_drawn += match['player_1']['draws']
        else:
            player_1_object = player_table.query.get(match['player_1']['id'])
            player_1_result_object = [item for item in tournament_result_objects if
                                      item.player_id == player_1_object.id]
            player_1_result_object[0].points += 3
            player_1_result_object[0].matches_won += 1
            player_1_result_object[0].games_won += match['player_2']['wins']
    db.session.commit()
    tournament_result_objects = tournament_result_table.query.filter_by(tournament_id=tournament_id).all()
    response_data = swiss_manager.create_tournament_ranking(tournament_results=tournament_result_objects,
                                                            player_table=player_table)
    return response_data


# Function for get_round_pairings()
def get_round_pairings(db, tournament_id: int, tournament_result_table: sqlalchemy.Model,
                       player_table: sqlalchemy.Model, match_table: sqlalchemy.Model, round_number: int):
    tournament_results = tournament_result_table.query.filter_by(tournament_id=tournament_id)
    pairings = swiss_manager.create_pairings(tournament_results=tournament_results, player_table=player_table)
    response_data = []
    for i in range(len(pairings)):
        match = match_table(
            tournament_id=tournament_id,
            round_number=round_number,
            table_number=i+1
        )
        db.session.add(match)
        for player in pairings[i]:
            if player != "Bye":
                player_object = player_table.query.get(player['id'])
                match.players.append(player_object)
        match_data = {
            'id': match.id,
            'round': match.round_number,
            'table_number': i + 1,
            'player_1': pairings[i][0],
            'player_2': pairings[i][1]
        }
        response_data.append(match_data)
    db.session.commit()
    return response_data


# Function for get_current_ranking()
def get_current_ranking(tournament_id: int, tournament_result_table: sqlalchemy.Model, player_table: sqlalchemy.Model):
    """
    Get current tournament rankings
    """
    tournament_result = tournament_result_table.query.filter_by(tournament_id=tournament_id).all()
    response_data = swiss_manager.create_tournament_ranking(tournament_results=tournament_result,
                                                            player_table=player_table)
    return response_data


# Function to create rows into TournamentResult
def create_tournament_result_rows(db: sqlalchemy, tournament_id: int, tournament_result_table: sqlalchemy.Model,
                                  player_table: sqlalchemy.Model, player_list: list) -> None:
    """
    Creates rows in the TournamentResult table for each player and sets results values to 0
    """
    for player in player_list:
        player_id = player['id']
        player_tour_result = tournament_result_table(
            tournament_id=tournament_id,
            player_id=player_id,
            points=0,
            matches_won=0,
            matches_drawn=0,
            games_won=0,
            games_drawn=0
        )
        db.session.add(player_tour_result)
    db.session.commit()


# # # - - - # # # - - - # # # - - - # # # - - - # # # - - - # # # - - - # # # - - - # # # - - #
# All the following functions are working but not actually implemented into the app for now - #
# # # - - - # # # - - - # # # - - - # # # - - - # # # - - - # # # - - - # # # - - - # # # - - #

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
