# Overview
# simulate card game

# Dependencies

# general
from datetime import datetime
from more_itertools import batched
import json
import logging
import os
from pathlib import Path

# mp
from concurrent.futures import ProcessPoolExecutor, wait
import multiprocessing as mp
from threading import Thread
from queue import Queue

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

def play_one_game(player):
    '''
    play one game

    player = player playing the game
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
    data = pd.DataFrame([d_data])

    return data

def consume():
    '''
    consumer: listen on the queue and write to db
    '''

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
    
        # listen and write
        while True:
            if not queue.empty():

                # get object to write
                i = queue.get()
                
                # write
                if isinstance(i, type(TERMINATION_SIGNAL)) and i == TERMINATION_SIGNAL:
                    # terminate
                    break
                elif isinstance(i, pd.DataFrame):
                    # write data
                    i.to_sql(
                        name = "simulations",
                        con = con,
                        if_exists = "append",
                        index = False,
                        dtype={
                            'state_initial': JSON,
                            'state_end': JSON,
                            },
                    )
                else:
                    raise TypeError(f"unsupported type ({type(i)})")

def produce(i):
    '''
    prodcer: either get data OR send termination signal

    i = player or termination signal
    '''
    
    if isinstance(i, type(TERMINATION_SIGNAL)) and i == TERMINATION_SIGNAL:
        # terminate
        queue.put(TERMINATION_SIGNAL)
    elif isinstance(i, Player):
        # get data
        queue.put(play_one_game(i))
    else:
        raise TypeError(f"unsupported type ({type(i)})")

if __name__ == "__main__":

    # set up logging
    logging.basicConfig(
        filename=PATH_OUTPUT_LOG,
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
        )
    logger = logging.getLogger(__name__)

    # set up queue
    manager = mp.Manager()
    queue = manager.Queue()

    # start consumer
    consumer = Thread(target=consume)
    consumer.daemon = True
    consumer.start()

    # with a pool executor
    # loop over players and number of simulations
    rng = range(NUM_SIMULATIONS)
    with ProcessPoolExecutor(max_workers = MAX_WORKERS) as executor:
        
        # submit jobs for each simulation
        for player in PLAYERS:
            batches = batched(rng, CHUNK_SIZE)
            for batch in batches:
                futures = [executor.submit(produce, player) for i in batch]
                wait(futures)  # wait for this batch to finish

        # after all legit jobs, send termination signal
        executor.submit(produce, TERMINATION_SIGNAL)

    # wait for jobs
    consumer.join()