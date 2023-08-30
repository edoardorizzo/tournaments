import json
from flask import request


def add_players_to_tournament_db(db, db_table):
    tournament = json.loads(request.get_json())
    tournament_name = tournament['name']
    player_names = tournament['players']
    for player_name in player_names:
        player = db_table(
            tournament=tournament_name,
            player=player_name
        )
        db.session.add(player)
    db.session.commit()
    response_data = {
        'tournament': db_table.tournament,
        'players': db.table.player
    }
    return response_data


def create_tournament(db, db_table):
    tournament_data = json.loads(request.get_json())
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


def add_players_to_db(db, db_table):
    player_data = json.loads(request.get_json())
    player_name = player_data['name']
    player = db_table(
        name=player_name
    )
    db.session.add(player)
    db.session.commit()
    response_data = {
        'id': player.id,
        'name': player.name
    }
    return response_data
