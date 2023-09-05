from flask import request


# Function for start_tournament()
def start_tournament(db, tournament_table, player_table):
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
def get_saved_players(db_table):
    """
    Returns a list of dictionaries containing player.id and player.name
    """
    players_objects = db_table.query.all()
    players = []
    if len(players_objects) > 0:
        for player in players_objects:
            player_dict = {'id': player.id, 'name': player.name}
            players.append(player_dict)
    return players


# Function to get saved tournaments
def get_saved_tournaments(db_table):
    tournaments_objects = db_table.query.all()
    tournaments = []
    if len(tournaments_objects) > 0:
        for tournament in tournaments_objects:
            tournament_dict = {'id': tournament.id, 'name': tournament.name, 'date': tournament.date}
            tournaments.append(tournament_dict)
    return tournaments


# All the following functions are working but not actually implemented into the app for now

def add_players_to_tournament_db(db, db_table):
    tournament = request.get_json()
    player_names = tournament['player_names']
    response_data = []
    for player_name in player_names:
        player = db_table(
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
def create_tournament(db, db_table):
    tournament_data = request.get_json()
    tournament = db_table(
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


# Function for add_players()
def add_players_to_db(db, db_table):
    player_data = request.get_json()
    response_data = []
    for player_name in player_data:
        player = db_table(
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


# Function for add_rounds()
def add_rounds_to_db(db, db_table):
    round_data = request.get_json()
    response_data = []
    for round_match in round_data:
        match = db_table(
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
