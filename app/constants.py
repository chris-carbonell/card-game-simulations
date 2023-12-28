# Dependencies

# general
from datetime import datetime
import os

# mp
import multiprocessing

# Constants

NUM_SIMULATIONS = 1000000

PATH_OUTPUT_LOG = f"./logs/{datetime.now().strftime('%Y-%m-%d %H%M%S')}.log"

MAX_WORKERS = multiprocessing.cpu_count()