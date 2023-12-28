# Dependencies

# general
from enum import Enum

# game
from pydealer.const import POKER_RANKS


class Guess(Enum):
    higher = 'higher'
    lower = 'lower'
    same = 'same'

# set ranks of cards based on values only
# https://pydealer.readthedocs.io/en/latest/usage.html#defining-new-rank-dictionaries
# unnecessary because default is POKER_RANKS:
# https://github.com/Trebek/pydealer/blob/master/pydealer/const.py#L31
RANKS = POKER_RANKS["values"]