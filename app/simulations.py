# Overview
# simulate card game

# Dependencies

# general
from datetime import datetime
import json
import logging
import os
from pathlib import Path

# mp
from concurrent.futures import ThreadPoolExecutor

# data
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, URL
from sqlalchemy.types import JSON

# game
from game.game import Game
from game.player import *

# constants
from constants import *

# Setup

# specify players to test
PLAYERS = [
    PlayerRandom(),
    PlayerModal(),
]

# Funcs

def play_one_game(player, con):
    '''
    play one game

    player = player playing the game
    con = SQLAlchemy connection
    '''

    # set up game
    logger.debug("starting game")
    game = Game(player)

    # save before
    state_initial = json.loads(str(game))

    # play
    logger.debug("playing game")
    game.play()

    # save end
    state_end = json.loads(str(game))

    # save results

    logger.debug("saving results")

    ## collect data
    d_data = {
            'dt_entered': datetime.now().strftime("%Y-%m-%d %H:%M:%SZ"),
            'player': str(game.player),

            'is_playable': game.is_playable,
            'player_won': game.player_won,

            'turns': game.turns,
            'lives': game.lives,

            'len_deck': len(game.deck),

            'state_initial': state_initial,
            'state_end': state_end,
        }

    ## save data to db
    data = pd.DataFrame([d_data])
    data.to_sql(
        name = "simulations",
        con = con,
        if_exists = "append",
        index = False,
        dtype={
            'state_initial': JSON,
            'state_end': JSON,
            },
    )

    return

if __name__ == "__main__":

    # set up logging
    logging.basicConfig(
        filename=PATH_OUTPUT_LOG,
        filemode="w",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
        )
    logger = logging.getLogger(__name__)

    # set up queue
    queue = Queue()

    # connect to db
    engine = create_engine(URL.create(
        drivername = "postgresql+psycopg2",
        host = os.environ['POSTGRES_HOST'], 
        port = os.environ['POSTGRES_PORT'], 
        database = os.environ['POSTGRES_DB'], 
        username = os.environ['POSTGRES_USER'], 
        password = os.environ['POSTGRES_PASSWORD'],
    ))
    with engine.connect() as con:

        # with a pool executor
        # loop over players and number of simulations
        with ThreadPoolExecutor(max_workers = MAX_WORKERS) as executor:
            for player in PLAYERS:
                for i in range(NUM_SIMULATIONS):

                    # play one game
                    executor.submit(play_one_game, player, con)