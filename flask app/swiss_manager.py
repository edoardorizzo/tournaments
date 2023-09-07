from flask_sqlalchemy import SQLAlchemy
import math
import random
import pandas as pd

sqlalchemy = SQLAlchemy()


def suggest_number_of_rounds(number: int) -> int:
    n_rounds = math.floor(math.log(number, 2))
    return n_rounds


def check_even_number(number: int) -> bool:
    remainder = number % 2
    if remainder == 0:
        return True
    else:
        return False


def first_round_pairings(player_list: list) -> list:
    random.shuffle(player_list)
    pairings = []
    for i in range(0, len(player_list), 2):
        if i + 1 < len(player_list):
            pairings.append((player_list[i], player_list[i+1]))
        else:
            pairings.append((player_list[i], "Bye"))
    return pairings


def create_pairings(tournament_results: list, player_table: sqlalchemy.Model):
    rankings = create_tournament_ranking(tournament_results=tournament_results, player_table=player_table)
    pairings = []
    for i in range(0, len(rankings), 2):
        if i + 1 < len(rankings):
            player_1_object = player_table.query.get(rankings[i]['player_id'])
            player_2_object = player_table.query.get(rankings[i + 1]['player_id'])
            player_1 = {'id': player_1_object.id, 'name': player_1_object.name}
            player_2 = {'id': player_1_object.id, 'name': player_2_object.name}
            pairings.append((player_1, player_2))
        else:
            player_1_object = player_table.query.get(rankings[i]['player_id'])
            player_1 = {'id': player_1_object.id, 'name': player_1_object.name}
            pairings.append((player_1, "Bye"))
    return pairings


def create_tournament_ranking(tournament_results: list, player_table: sqlalchemy.Model) -> list:
    rows_dict = [row.__dict__ for row in tournament_results]
    for i in rows_dict:
        player_object = player_table.query.get(i['player_id'])
        i['player_name'] = player_object.name
        i.pop('_sa_instance_state', None)
        i.pop('tournament_id', None)
    df = pd.DataFrame.from_records(rows_dict, index='id')
    position = []
    df = df.sort_values(by=['points', 'matches_won', 'games_won'], ascending=False)
    for i in range(df.shape[0]):
        position.append(i + 1)
    df['position'] = position
    new_order = ['position', 'player_id', 'player_name', 'points', 'matches_won', 'games_won', 'matches_drawn']
    df = df[new_order]
    dictionary = df.to_dict('records')
    return dictionary
