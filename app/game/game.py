# Dependencies

# general
from collections import UserDict
import json
import logging

# game
import pydealer
from .constants import Guess, RANKS

# Setup

logging.getLogger(__name__)

# Classes

class Stack(pydealer.Stack):
    '''
    stack with liveness
    '''

    def __init__(self):
        super(Stack, self).__init__()
        self.is_alive = True

class Gauntlet(UserDict):
    '''
    the gauntlet
    manages stacks and status of each stack
    '''

    def __init__(self, n = 9):
        '''
        n = number of stacks in the gauntlet
        '''
        self.data = {i: Stack() for i in range(n)}  # dict of empty stacks

    def __str__(self):
        '''
        print the gauntlet
        '''
        d = {}
        for idx, stack in self.data.items():
            d[idx] = {
                # status/liveness
                'is_alive': stack.is_alive,
                # top = card to for comparison basis
                'top': str(stack[-1]) if len(stack) > 0 else None,
                # discarded = prior cards
                'discarded': [str(card) for card in reversed(stack[0:-1])]
            }
        return json.dumps(d, indent = 2)

    def __repr__(self):
        '''
        print the gauntlet
        '''
        return str(self)

class Game():
    '''
    game
    '''

    def __init__(self, player):
        '''
        set up the game
        '''

        # basics
        self.turns = 0
        self._is_playable = True
        self.player_won = False
        
        # set up draw pile aka deck
        deck = pydealer.Deck()
        deck.shuffle()
        self.deck = deck

        # set up gauntlet
        gauntlet = Gauntlet()
        for idx, stack in gauntlet.items():
            stack.add(self.deck.deal()[-1])
        self.gauntlet = gauntlet

        # player
        self.player = player

    def __str__(self):
        
        # game details
        d_game = {
            'is_playable': self.is_playable,
            'player_won': self.player_won,
        }

        # stack info
        d_stacks = {
            'gauntlet': json.loads(str(self.gauntlet)),
            'deck': [str(card) for card in reversed(self.deck)],
        }

        # combine
        d = {
            'game': d_game,
            'stacks': d_stacks,
        }
        
        return json.dumps(d, indent = 2)

    @property
    def lives(self):
        return sum([stack.is_alive for idx, stack in self.gauntlet.items()])

    @property
    def is_playable(self):
        return any([stack.is_alive for idx, stack in self.gauntlet.items()])

    def step(self):
        '''
        step through one guess
        '''

        # get player's guess
        idx_stack, guess = self.player.guess(self)

        # judge the guess
        next_card = self.deck.deal()[-1]
        correct_guess = self.judge_guess(idx_stack, next_card, guess)

        # process
        self.gauntlet[idx_stack].add(next_card)  # add card to the target stack
        if correct_guess:
            # correct guess
            if len(self.deck) == 0:
                # correctly guessed the last card
                # so player wins
                self.player_won = True
                logging_message = "player wins!"
            else:
                # correctly guessed the card
                # and more cards remain in the gauntlet
                logging_message = "player guessed correctly! moving on to next target"
                pass
        else:
            # incorrect guess
            self.gauntlet[idx_stack].is_alive = False
            logging_message = "player guessed incorrectly :( removing life"

        # increment counter
        self.turns += 1

        # log
        logging.debug(logging_message + "\n")
        
        return
    
    def judge_guess(self, idx_stack, card_target, guess):
        '''
        judge player's guess

        idx_stack = index of stack in gauntlet the player is guessing on
        card_target = card on which to judge the guess (i.e., card drawn from draw pile)
        guess = the guess for that stack
        '''

        # get cards
        card_base = self.gauntlet[idx_stack][-1]  # prior card

        # get reality
        if card_target.gt(card_base, RANKS):
            reality = Guess.higher
        elif card_target.lt(card_base, RANKS):
            reality = Guess.lower
        else:
            reality = Guess.same

        # log
        logging.debug(f"idx_stack: {idx_stack}")
        logging.debug(f"card_base: {str(card_base)}")
        logging.debug(f"card_target: {str(card_target)}")
        logging.debug(f"reality: {reality}")
        logging.debug(f"guess: {guess}")

        return guess == reality

    def play(self, n_steps: int = None):
        '''
        play out the entire game

        n_steps = number of steps to play (default = play whole game)
        '''

        # continue to play the game if:
        # 1. the game is playable (i.e., enough cards to fill the gauntlet)
        # 2. the player has not won yet
        n = 0  # step tracker
        while self.is_playable and not self.player_won:
            logging.debug(f"n: {n}")
            if n_steps is None:
                self.step()
            else:
                if n < n_steps:
                    self.step()
                else:
                    break
            n += 1