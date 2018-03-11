# Initial primary code for command line Blackjack - might split into separate files if necessary
# A Game has Players, a Dealer and a Deck of Cards
# A Player has Cards and set of actions
# A Deck has Cards or is Empty
from random import shuffle

class Player():

  # name can be either Player's real name, or default "Player 1"/"Dealer" which are automatically assigned

  def __init__(self):
      self.name = None
      self.currentValue = 0
      self.hand = None

  def show_hand(self):
      for card in hand:
          print(card)

  def count_hand(self):
      print(None)

class Hand():
  def __init__(self):
      self.cards = {'fixedCards':[], 'aces': []}
      self.value = 0

  # iterate through all cards and sum hand value
  def calculate_value(self):
      for key in self.cards:
          for card in self.cards[key]:
              value += card.value

      # if resulting hand value over 21, and there is at least one ace
      if self.value > 21 and len(self.cards['aces']) > 0:
          change_aces()

  # called if hand exceeds 21 and holding aces. Change aces to 1 until hand less than 21
  def change_aces(self):
      for card in cards['aces']:
          if card.value == 11:
              card.value = 1
              calculate_value()
          if value <= 21:
              break
            
class Deck():

  # code
  def __init__(self):
    self.cards = []
    self.suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
    self.types = ['King', ' Queen', 'Jack', 'Ace']

  def build(self):
    for suit in self.suits:
      # standard cards
      for x in range(0,11):
        self.cards.append(Card(suit,x))

      # special cards
      for cardType in self.types:
        value = 0
        if cardType == 'Ace':
          value = 11
        else:
          value = 10
        self.cards.append(Card(cardType,value))

    # can I use list comprehension?
    # subclass of Card? Special card with extra attribute for Type?
    # cards = [self.suits for self.suits in range(0,11)]
    for card in self.cards:
      print(str(card.value) + " of " + card.suit)

  def shuffle(self):
    return None
      # code

class Card():

  # all cards have suit (clubs, spades, diamonds, hearts) and a value (number, or special class)

  def __init__(self, suit, value):
    self.suit = suit
    self.value = value

class Game():
  def __init__(self):
    self.players = [Player(), Player()]
    self.deck = Deck()
    self.won = False

  def deal_player(self):
    return None
    # deal card from Deck to Player's Hand
    # if card is Ace, check Hand value

  def start_game(self):
    return None
    # get Player(s) name(s)
    # create Deck
    # create Cards
    # shuffle Cards

  def check_win(self):
    return None
    # code

  def end_game(self):
    return None
    # code
  
  def reset_game(self):
    return None
    # code

# Game logic

deck = Deck()

deck.build()

# Player enters name
# Cards created
# Cards shuffled
# Cards dealt
# Continue to calculate hand for every Card dealt
# If either exceeds 21, other Player wins
# If either Player or Dealer hit 21, they win. Dealer wins if both are 21

##
