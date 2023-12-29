# Dependencies

# general
from datetime import datetime
import os

# mp
import multiprocessing

# Constants

NUM_SIMULATIONS = 10**6
CHUNK_SIZE = 10**4

PATH_OUTPUT_LOG = f"./logs/simulations.log"

MAX_WORKERS = multiprocessing.cpu_count()

TERMINATION_SIGNAL = "et tu brute"