from flask import request


# Function for start_tournament()
def add_players_to_tournament_db(db, db_table):
    tournament = request.get_json()
    player_names = tournament['players']
    for player_name in player_names:
        player = db_table(
            tournament=tournament['name'],
            player=player_name
        )
        db.session.add(player)
    db.session.commit()
    response_data = {
        'tournament': db_table.tournament,
        'players': db.table.player
    }
    return response_data


# Function for create_tournaments()
def create_tournament(db, db_table):
    tournament_data = request.get_json()
    tournament_name = tournament_data['name']
    tournament_date = tournament_data['date']
    tournament = db_table(
        name=tournament_name,
        date=tournament_date
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
    player = db_table(
        name=player_data['name']
    )
    db.session.add(player)
    db.session.commit()
    response_data = {
        'id': player.id,
        'name': player.name
    }
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
