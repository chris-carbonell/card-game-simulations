# Overview
simulate a made-up card game

# The Game
Refer to this doc ([link](app/game/README.md)) for the game's objective and rules.

# Why?
* determine the probability of winning to feel better about losing
    * compare random guessing to educated guessing
* figure out how to efficiently simulate <b>two million</b> games by taking advantage of:
    * a PostgresSQL db in a Docker container
        * using a db simplified the coding around concurrent events (e.g., saving data) 
    * multiprocessing in Python (my server has 4 CPUs)
        * I reserved one CPU for the consumer so I boosted the speed of the simulations by about 3 times.
    * consumer-producer pattern
        * allowing each producer to focus on just simulating games doubled simulation speed

# Questions
1. What's the probability of the Player winning if they guess randomly?
1. What's the probability of the Player winning if they remember every card played so far?
    * The Player would then know the probability of the next card from the Draw Pile being higher or lower and could guess accordingly.
    * The Player would obviously not know the actual value of the next card from the Draw Pile.

# Roadmap
* clean up logging