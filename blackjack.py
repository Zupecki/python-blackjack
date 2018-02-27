# Initial primary code for command line Blackjack - might split into separate files if necessary
# A Game has Players, a Dealer and a Table
# A Table has a Deck and state of Cards
# A Player has Cards and set of actions
# A Dealer has Cards and set of actions
# A Deck has Cards or is Empty


class Table:

    # code

    def __init__(self):
        self.players = []
        self.cards = []
        self.score = 0

class Player:

    # can be either Player's real name, or default "Player 1"/"Dealer" which are automatically assigned

    def __init__(self):
        self.cards = []
        self.name = None
        self.currentValue = 0

    def show_cards(self):
        for card in cards:
            print(card)

    def __str__(self):
        # print Player object in formatted form

class Deck:

    # code
    def __init__(self):
        self.cards = []

class Card:

    # all cards have suit (clubs, spades, diamonds, hearts) and a value (number, or special class)

    def __init__(self):
        suit = None
        value = None

class Game:

    # code
    def __init__(self):
        self.players = []
        self.deck = None
        self.table = None

    def start_game():
        # code

    def check_win():
        # code

    def end_game():
        # code
    
    def reset_game():
        # code

# Game logic

##
