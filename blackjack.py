# Initial primary code for command line Blackjack - might split into separate files if necessary
# A Game has Players, a Dealer and a Deck of Cards
# A Player has Cards and set of actions
# A Deck has Cards or is Empty
from random import shuffle

class Player():

  # name can be either Player's real name, or default "Player 1"/"Dealer" which are automatically assigned

  def __init__(self):
      self.name = None
      self.hand = None

  def show_hand(self):
      for card in hand:
          print(card)

  def hand_value(self):
    self.hand

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

  # cycle through cards in deck, call their string output
  def __str__(self):
    for cardType in self.cards:
      for card in cardType:
        card.__str__()
            
class Deck():

  # code
  def __init__(self):
    self.cards = []
    self.suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
    self.kinds = ['King', 'Queen', 'Jack', 'Ace']

  def build(self):
    for suit in self.suits:
      # standard cards
      kind = None
      for value in range(2,11):
        self.cards.append(Card(suit,value,kind))

      # special cards
      for kind in self.kinds:
        value = 0
        if kind == 'Ace':
          value = 11
        else:
          value = 10
        self.cards.append(Card(suit,value,kind))

    # can I use list comprehension?
    # cards = [self.suits for self.suits in range(0,11)]

  def shuffle(self):
    return None
      # code

  # stringify Deck by calling each Card stringify
  def __str__(self):
    for card in self.cards:
      card.__str__()

class Card():

  # all cards have suit (clubs, spades, diamonds, hearts) and a value (number, or special class)
  def __init__(self, suit, value, kind):
    self.suit = suit
    self.value = value
    self.kind = kind

  # print cards in correct format
  def __str__(self):
    if(self.kind == None):
      print("{} of {} - ({})".format(str(self.value), self.suit, self.value))
    else:
      print("{} of {} - ({})".format(self.kind, self.suit, self.value))

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

deck.__str__()

# Player enters name
# Cards created
# Cards shuffled
# Cards dealt
# Continue to calculate hand for every Card dealt
# If either exceeds 21, other Player wins
# If either Player or Dealer hit 21, they win. Dealer wins if both are 21

##
