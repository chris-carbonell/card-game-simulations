# Dependencies

# general
# import logging
import random

# game
import pydealer
from .game import Game
from .constants import Guess, RANKS

# Classes

class Player():
    '''
    base player
    '''
    
    def pick_stack(self):
        '''
        pick a stack on which to base the guess
        '''
        raise NotImplementedError
    
    def guess(self):
        '''
        guess higher or lower
        '''
        raise NotImplementedError

    def __str__(self):
        '''
        make it easy to log the player details/settings
        '''
        raise NotImplementedError

class PlayerRandom(Player):
    '''
    player that guesses randomly
    '''

    def __init__(self, p_higher = 0.5):
        '''
        p_higher = probability of guessing higher
        '''
        self.p_higher = p_higher

    def pick_stack(self, game: Game):
        '''
        pick randomly
        can only choose among alive stacks
        '''
        alive_stacks = [idx for idx, stack in game.gauntlet.items() if stack.is_alive]
        return random.choice(alive_stacks)
    
    def guess(self, game: Game):
        '''
        guess randomly
        '''

        # stack
        idx_stack = self.pick_stack(game)

        # guess
        if random.random() >= self.p_higher:
            guess = Guess.higher
        else:
            guess = Guess.lower

        return (idx_stack, guess)

    def __str__(self):
        return f"PlayerRandom(p_higher={self.p_higher})"

class PlayerModal(Player):
    '''
    player that guesses the most likely option
    with knowledge of the proportion of values in the deck
    '''

    def get_deck_percs(
        self, 
        card_base: pydealer.Card, 
        deck: pydealer.Deck, 
        ):
        '''
        get percentage of higher cards left in play

        card_base = card to compare against (i.e., card in gauntlet)
        deck = draw pile on which to base percentages of higher/lower
        '''

        # get cards remaining
        cards_remaining = len(deck)

        # perc_lower
        perc_lower = round(sum([card.lt(card_base, RANKS) for card in deck]) / cards_remaining, 2)

        # perc_same
        perc_same = round(sum([card.eq(card_base, RANKS) for card in deck]) / cards_remaining, 2)

        # perc_higher
        perc_higher = round(1 - perc_lower - perc_same, 2)

        # # log
        # logging.debug(f"card_base = {str(card_base)}")
        # logging.debug(f"perc_lower = {perc_lower}")
        # logging.debug(f"perc_same = {perc_same}")
        # logging.debug(f"perc_higher = {perc_higher}")
        # # logging.debug(f"game.deck = {str(game.deck)}")

        return (perc_lower, perc_same, perc_higher)

    def pick_stack(self, game: Game):
        '''
        pick stack with highest chance of success
        '''

        # find ultimate
        ultimate_idx = None  # idx of stack on which to guess for best chance of success
        ultimate_perc = 0  # the biggest perc for highers/lowers
        ultimate_higher = None  # True = higher, False = lower
        for idx, stack in game.gauntlet.items():
            
            # only process alive stacks (i.e., active / in play)
            if stack.is_alive:
                
                # get percs
                perc_lower, perc_same, perc_higher = self.get_deck_percs(
                    stack[-1],
                    game.deck,
                )

                # set ultimate
                if perc_higher >= perc_lower and perc_higher > ultimate_perc:
                    # higher
                    # if tie between higher and lower, go with higher
                    ultimate_idx = idx
                    ultimte_perc = perc_higher
                    ultimate_higher = True
                elif perc_lower > perc_higher and perc_lower > ultimate_perc:
                    # lower
                    ultimate_idx = idx
                    ultimte_perc = perc_lower
                    ultimate_higher = False
                else:
                    # same
                    pass

        return (ultimate_idx, ultimate_perc, ultimate_higher)

    def guess(self, game: Game):
        '''
        guess the most likely (modal)
        based on the proportion of higher and lower cards left in play
        i.e., cards not seen yet
        '''

        # pick stack
        ultimate_idx, ultimate_perc, ultimate_higher = self.pick_stack(game)

        # parse
        if ultimate_higher:
            guess = Guess.higher
        else:
            guess = Guess.lower

        return (ultimate_idx, guess)

    def __str__(self):
        return f"PlayerModal()"