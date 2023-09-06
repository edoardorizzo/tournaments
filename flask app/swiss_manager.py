from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
import random
import pandas as pd

db = SQLAlchemy()


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


def create_tournament_ranking(tournament_results: list):
    rows_dict = [row.__dict__ for row in tournament_results]
    for i in rows_dict:
        i.pop('_sa_instance_state', None)
        i.pop('tournament_id', None)
    df = pd.DataFrame.from_records(rows_dict, index='id')
    position = []
    df = df.sort_values(by=['points', 'matches_won', 'games_won'], ascending=False)
    for i in range(df.shape[0]):
        position.append(i + 1)
    df['position'] = position
    new_order = ['position', 'player_id', 'points', 'matches_won', 'games_won', 'matches_drawn']
    df = df[new_order]
    dictionary = df.to_dict('records')
    return dictionary
