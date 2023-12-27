# Overview
simulate a made-up card game to feel better about losing

# Rules

This is basically a one person game. The player - <b>the Guesser</b> - guesses cards. Another player - <b>the Dealer</b> - simply deals the cards.
1. The Dealer deals 9 cards face down in a line to form the Gauntlet.
1. The Dealer flips over the first (leftmost) card in the Gauntlet.
1. The Guesser guesses if the next card (the second card from the left) is higher or lower than the first card.
    * If the Guesser guesses correctly, play continues with the third card, fourth card, and so on.
    * If the Guesser guess incorrectly, all but the first card are replenished with face down cards.
        * If the next card ties the prior card (e.g., they're both aces), the Guesser guessed incorrectly.
1. The Guesser wins if they correctly guess higher or lower on all of the 8 cards. The Guesser loses if they run out of cards to replenish the Gauntlet.

# Questions
1. What's the probability of the Guesser winning if they guess randomly?
1. What's the probability of the Guesser winning if they remember every card played so far?
    * The Guesser would then know the probability of the next card being higher or lower and could guess accordingly.
    * The Guesser would obviously not know the actual value of the next card.