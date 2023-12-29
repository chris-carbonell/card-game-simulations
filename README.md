# Overview
simulate a made-up card game

# Executive Summary
* process
   * we can increase the number of simulations per second from about 0.5 to about 100.0 (a <b>200x improvement</b>)
* game
   * educated guessing (i.e., counting cards) - the best one could do without cheating - wins about <b>11.2%</b> of the time
   * choosing the most extreme card (e.g., the highest) and simply guessing in the appropriate direction (e.g., lower) wins about <b>5.6</b>% of the time
   * if you win, on average, you're <b>left with just 2 lives</b> (i.e., you use up 7 out of 9)
   * if you lose, on average, you leave about 14 cards in the Draw Pile

# The Game
Refer to this doc ([link](app/game/README.md)) for the game's objective and rules.

# Why?
* determine the probability of winning to feel better about losing
    * compare random guessing to educated guessing
* figure out how to efficiently simulate <b>three million</b> games by taking advantage of:
    * a PostgresSQL db in a Docker container
        * using a db simplified the coding around concurrent events (e.g., saving data)
    * multiprocessing in Python
    * consumer-producer pattern
        * allowing each producer to focus on just simulating games doubled simulation speed
    * batching and futures
        * the process pool can get flooded with jobs so I batched them to make them easier to digest

# Questions
1. What's the probability of the Player winning if they guess randomly?
1. What's the probability of the Player winning if they remember every card played so far?
    * The Player would then know the probability of the next card from the Draw Pile being higher or lower and could guess accordingly.
    * The Player would obviously not know the actual value of the next card from the Draw Pile.

# Roadmap
* clean up logging
