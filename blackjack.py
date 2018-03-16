# Initial primary code for command line Blackjack - might split into separate files if necessary
# A Game has Players, a Dealer and a Deck of Cards
# A Player has Cards and set of actions
# A Deck has Cards or is Empty
from random import shuffle

# misc global functions - probably best in own file

# convert int num to word-string version
def num_to_word(num):
  ref = {0:"Zero",1:"One",2:"Two",3:"Three",4:"Four",5:"Five",
  6:"Six",7:"Seven",8:"Eight",9:"Nine",10:"Ten"}

  return ref[num]

class Player():

  def __init__(self, name):
      self.name = name
      self.hand = Hand()

  def show_hand(self):
    for key, value in self.hand.cards.items():
      for card in value:
        print(card)

  def hand_value(self):
    self.hand

# Dealer subcalass of Player with special features
class Dealer(Player):

  def __init__(self, name, deck):
    Player.__init__(self, name)
    self.deck = deck

  def deal_card(self, player):
    card = self.deck.pop_card()

    if(card.title != "Ace"):
      cardType = "fixedCards"
    else:
      cardType = "aces"

    player.hand.cards[cardType].append(card)
    player.hand.count += 1
    print("{} - popped from deck and given to {}".format(card, player.name))

  def shuffle_deck(self):
    return None

class Hand():
  def __init__(self):
      self.cards = {'fixedCards':[], 'aces': []}
      self.value = 0
      self.count = 0

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

  def __init__(self):
    self.cards = []
    self.count = None

  def build(self):
    suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
    kinds = ['King', 'Queen', 'Jack', 'Ace']

    for suit in suits:
      # standard cards
      for value in range(2,11):
        title = num_to_word(value)
        self.cards.append(Card(suit, value, title))

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
  def __init__(self, suit, value, title):
    self.suit = suit
    self.value = value
    self.title = title
    # adding attributes for potential art to be added
    self.art = None
    self.pos = [None, None]

  # print card in correct format
  def __str__(self):
    return "{} of {} - ({})".format(self.title, self.suit, self.value)

class Game():
  def __init__(self):
    self.players = ()
    self.dealer = None
    self.won = False

  def deal(self):
    return None
    # deal card from Deck to Player's Hand
    # if card is Ace, check Hand value

  def start(self):
    return None

  def setup(self):
    # get Player's name
    print("Welcome to Python Blackjack, also known colloquially as Twenty One!\nPlease enter your name:")
    name = input()
    self.players = (Player(name),)

    # Deck
    deck = Deck()
    deck.build()
    deck.shuffle()

    # create Dealer and give deck
    self.dealer = Dealer("Dealer", deck)

  def check_win(self):
    return None
    # code

  def end(self):
    return None
    # code
  
  def reset(self):
    return None
    # code

  # give card to Player, update Hand
  def give_card(self, card, player):
    if(card.title != "Ace"):
      cardType = "fixedCards"
    else:
      cardType = "aces"

    player.hand.cards[cardType].append(card)
    player.hand.count += 1
# Game logic

# Build game object, then set it up with Players, Dealer and Deck
game = Game()
game.setup()

print("\n")
# show Deck for testing
game.dealer.deck.show_cards()
print("\n{} cards in the deck.\n".format(game.dealer.deck.count))

# card 1
game.dealer.deal_card(game.players[0])

# card 2
game.dealer.deal_card(game.players[0])

# show hand
print("\n{} holding {} cards in Hand:".format(game.players[0].name, str(game.players[0].hand.count)))
game.players[0].show_hand()

# report how many cards are in the deck
print("\n{} cards in the deck.\n".format(game.dealer.deck.count))

print("Player's name is {}".format(game.players[0].name))
print("Player's name is {}".format(game.dealer.name))

# Player enters name - how many players? **kwargs? (["Michael": 1, "Jason": 2"]) etc? Or **args? (["Michael, Jason"]) etc?
# Cards created
# Cards shuffled
# Cards dealt
# Continue to calculate hand for every Card dealt
# If either exceeds 21, other Player wins
# If either Player or Dealer hit 21, they win. Dealer wins if both are 21

##
