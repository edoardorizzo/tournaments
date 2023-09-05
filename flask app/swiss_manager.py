from flask_sqlalchemy import SQLAlchemy
import random

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

