# Initial primary code for command line Blackjack - might split into separate files if necessary
# A Game has Players, a Dealer and a Deck of Cards
# A Player has Cards and set of actions
# A Deck has Cards or is Empty
from random import shuffle

class Player():

  # name can be either Player's real name, or default "Player 1"/"Dealer" which are automatically assigned

  def __init__(self, name):
      self.name = name
      self.hand = Hand()

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

  # cycle through cards in Hand, call their string output
  def show_hand(self):
    for cardType in self.cards:
      for card in cardType:
        print(card)
            
class Deck():

  def __init__(self):
    self.cards = []
    self.count = None

  def build(self):
    suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
    kinds = ['King', 'Queen', 'Jack', 'Ace']

    for suit in suits:
      # standard cards
      for value in range(2,11):
        self.cards.append(Card(suit, value, None))

      # special cards
      for kind in kinds:
        if kind == 'Ace':
          value = 11
        else:
          value = 10
        self.cards.append(Card(suit, value, kind))

    # commit initial Deck length to keep track of card count
    self.count = len(self.cards)

    # can I use list comprehension?
    # cards = [self.suits for self.suits in range(0,11)]

  def shuffle(self):
    shuffle(self.cards)

  # remove Card from Deck, return it
  def pop_card(self):
    card = self.cards.pop()
    self.count -= 1
    return card

  # stringify Deck by calling each Card stringify
  def show_cards(self):
    for card in self.cards:
      print(card)

class Card():

  # all cards have suit (clubs, spades, diamonds, hearts) and a value (number, or special class)
  def __init__(self, suit, value, kind):
    self.suit = suit
    self.value = value
    self.kind = kind

  # print card in correct format
  def __str__(self):
    if(self.kind == None):
      return "{} of {} - ({})".format(str(self.value), self.suit, self.value)
    else:
      return "{} of {} - ({})".format(self.kind, self.suit, self.value)

class Game():
  def __init__(self):
    self.players = ()
    self.deck = Deck()
    self.won = False

  def deal(self):
    return None
    # deal card from Deck to Player's Hand
    # if card is Ace, check Hand value

  def start(self):
    # get Player's name
    print("Welcome to Python Blackjack, also known colloquially as Twenty One!\nPlease enter your name:")
    self.players = (Player("Dealer"), Player(input()))

    # Deck
    self.deck.build()
    self.deck.shuffle()

  def check_win(self):
    return None
    # code

  def end(self):
    return None
    # code
  
  def reset(self):
    return None
    # code

# Game logic

# Build and shuffle deck - to go inside Game object in game.start()
game = Game()
game.start()

print("\n")
game.deck.show_cards()

print("\n{} cards in the deck.\n".format(game.deck.count))

card = game.deck.pop_card()
print("{} - popped from deck".format(card))

print("\n{} cards in the deck.\n".format(game.deck.count))

print("Player's name is {}".format(game.players[0].name))
print("Player's name is {}".format(game.players[1].name))

# Player enters name - how many players? **kwargs? (["Michael": 1, "Jason": 2"]) etc? Or **args? (["Michael, Jason"]) etc?
# Cards created
# Cards shuffled
# Cards dealt
# Continue to calculate hand for every Card dealt
# If either exceeds 21, other Player wins
# If either Player or Dealer hit 21, they win. Dealer wins if both are 21

##
