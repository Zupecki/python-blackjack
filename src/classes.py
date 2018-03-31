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
      self.bust = False
      self.blackjack = False
      self.cash = 0

  def show_hand(self):
    print("\n{} holding {} cards in Hand:".format(self.name, str(self.hand.count)))
    for key, value in self.hand.cards.items():
      for card in value:
        print(card)

  def insert_card(self, card):
    if(card.title != "Ace"):
      cardType = "fixedCards"
    else:
      cardType = "aces"

    # add card to player's hand, update hand stats, assign bust or not
    self.hand.cards[cardType].append(card)
    self.update_hand()

  def update_hand(self):
    # update hand
    self.hand.count += 1
    self.hand.recalculate_value()
    state = self.hand.check_hand()

    if(state == 'blackjack'):
      self.blackjack = True
    elif(state == 'bust'):
      self.bust = True

  def get_name(self):
    return self.name

  def __str__(self):
    return "Name: {}\nHand value: {}\nCash: {}\n".format(self.name, self.hand.value, self.cash)

# Dealer subcalass of Player with special features
class Dealer(Player):

  def __init__(self, name):
    Player.__init__(self, name)

  def deal_card(self, player, deck, faceDown):
    card = deck.pop_card()
    card.faceDown = faceDown
    player.insert_card(card)
    # print("{} - removed from deck and dealt to {}".format(card, player.name))

class Hand():
  def __init__(self):
      self.cards = {'fixedCards':[], 'aces': []}
      self.value = 0
      self.count = 0

  # iterate through all cards and sum hand value
  def recalculate_value(self):
    self.value = 0

    # sum value of cards
    for key in self.cards:
      # sum value of all cards
      for card in self.cards[key]:
        self.value += card.value

      # if hand value over 21, and there is at least one ace, else bust!
      if self.value > 21 and len(self.cards['aces']) > 0:
        self.change_aces()

  # called if hand exceeds 21 and holding aces. Change aces to 1 until hand less than 21
  def change_aces(self):
    for card in self.cards['aces']:
      if card.value == 11:
        # if ace still 11, reduce to 1 and subtract difference from hand value
        card.value = 1
        self.value -= 10
        # if hand now acceptable, stop iterating
      if self.value <= 21:
        break
    
  # check if hand is bust or blackjack (loss/win)
  def check_hand(self):
    if(self.value == 21):
      return 'blackjack'
    elif self.value > 21:
      return 'bust'
    else:
      return None
            
class Deck():

  def __init__(self):
    self.cards = []
    self.count = 0

  def build(self):
    suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
    faces = ['King', 'Queen', 'Jack', 'Ace']

    for suit in suits:
      # standard cards
      for value in range(2,11):
        title = num_to_word(value)
        self.cards.append(Card(suit, value, title))

      # special cards
      for face in faces:
        if face == 'Ace':
          value = 11
        else:
          value = 10
        self.cards.append(Card(suit, value, face))

    # commit initial Deck length to keep track of card count
    self.count = len(self.cards)

    # can I use list comprehension?
    # cards = [self.suits for self.suits in range(0,11)]

  def shuffle(self):
    shuffle(self.cards)

  # remove Card from Deck, if there are Cards, return it
  def pop_card(self):
    if(self.count <= 0):
      raise IndexError("Deck has no more cards")
    else:
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
    self.faceDown = False
    # adding attributes for potential art to be added
    self.art = None
    self.pos = [None, None]

  # print card in correct format
  def __str__(self):
    return "{} of {} - ({})".format(self.title, self.suit, self.value)

class Game():
  def __init__(self):
    self.players = None
    self.dealer = None
    self.deck = None
    self.won = False
    self.buyIn = 0
    self.multi = False

  def setup(self):
    # welcome message and Player creation
    print("Welcome to Python Blackjack, also known colloquially as Twenty One!")

    # Players
    self.players = self.create_players()

    # Deck
    self.deck = self.create_deck()

    # Dealer
    self.dealer = Dealer("Dealer")

    # Buy in
    self.buyIn = self.assign_cash()

  def initial_deal(self):
    for x in range(0,2):
      faceDown = False
      for player in self.players:
        self.dealer.deal_card(player, self.deck, faceDown)
      if(x == 1):
        faceDown = True
      self.dealer.deal_card(self.dealer, self.deck, faceDown)

    #for key, value in self.dealer.hand.cards.items():
    #  for card in value:

  def assign_cash(self):
    print("What is the buy in? (Cash each Player starts with)")

    while True:
      try:
        cash = int(input())
      except ValueError:
        print("Must be a number, try again.\nHow much cash does each Player have?")
        continue
      else:
        break

    for player in self.players:
      player.cash = cash

    self.dealer.cash = cash

    return cash

  def create_players(self):
    players = ()
    num = 0

    # multiplayer if game.multi = True
    if(self.multi != False):
      print("How many players?")

      # validate that input is a number by casting to int and capturing exception
      while True:
        try:
          num = int(input())
        except ValueError:
          print("Must be a number, try again.\nHow many players?")
          continue
        else:
          break
    else:
      num = 1

    # cycle through and create Player's with names
    for x in range(1,num+1):
      print("What is Player {}'s name?".format(x))
      name = input()
      # concatenate as new tuple to allow for incremental tuple to be returned with all players
      players = players + (Player(name),)

    return players

  def create_deck(self):
    deck = Deck()
    deck.build()
    deck.shuffle()

    return deck

  def start(self):
    return None

  def check_win(self):
    return None
    # check for winner, report busted Player's
    # ask remaining players to check or hit

  def end(self):
    return None
    # code
  
  def reset(self):
    return None
    # code

  def print_players(self):
    for player in self.players:
      print(player)
    print(self.dealer)

  def show_players_hands(self):
    for player in self.players:
      player.show_hand()
    self.dealer.show_hand()