# Initial primary code for command line Blackjack - might split into separate files if necessary
# A Game has Players, a Dealer and a Deck of Cards
# A Player has Cards and set of actions
# A Deck has Cards or is Empty
from random import shuffle

class Player:

    # name can be either Player's real name, or default "Player 1"/"Dealer" which are automatically assigned

    def __init__(self):
        self.name = None
        self.currentValue = 0
        self.hand = None

    def show_hand(self):
        for card in hand:
            print(card)

    def count_hand(self):
        # code

    def __str__(self):
        # print Player object in formatted form

class Hand:

    def __init__(self):
        self.cards = {'fixedCards':[], 'aces': []}
        self.value = 0

    # iterate through all cards and sum hand value
    def calculate_value(self):
        for card in cards['fixedCards']:
            value += card.value
        for card in cards['aces']:
            value += card.value

    # called if hand exceeds 21 and holding aces. Change aces to 1 until hand less than 21
    def ace_value(self):
        for card in cards['aces']:
            if card.value == 11:
                card.value = 1
                calculate_value():
            if value <= 21:
                break
            

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

    def deal_player(self):
        # deal card from Deck to Player's Hand
        # if card is Ace, check Hand value

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
