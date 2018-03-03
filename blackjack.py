# Initial primary code for command line Blackjack - might split into separate files if necessary
# A Game has Players, a Dealer and a Table
# A Table has a Deck and state of Cards
# A Player has Cards and set of actions
# A Dealer has Cards and set of actions
# A Deck has Cards or is Empty
from random import shuffle

class Player:

    # name can be either Player's real name, or default "Player 1"/"Dealer" which are automatically assigned

    def __init__(self):
        self.cards = []
        self.name = None
        self.currentValue = 0

    def show_hand(self):
        for card in cards:
            print(card)

    def count_hand(self):
        # code

    def __str__(self):
        # print Player object in formatted form

class Deck:

    # code
    def __init__(self):
        self.cards = []

    def build_deck(self):
        # code

    def shuffle_deck(self):
        # code

class Card:

    # all cards have suit (clubs, spades, diamonds, hearts) and a value (number, or special class)

    def __init__(self):
        suit = None
        value = None

class Game:
    def __init__(self):
        self.players = []
        self.deck = None
        self.won = False

    def start_game(self):
        # code

    def check_win(self):
        # code

    def end_game(self):
        # code
    
    def reset_game(self):
        # code

# Game logic

##
