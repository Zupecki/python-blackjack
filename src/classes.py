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

  def __init__(self, name, num):
    self.num = num
    self.name = name
    self.hands = (Hand(), )
    self.states = {'Bust': False, 'Blackjack': False, 'Double': False}
    self.playing = True
    self.cash = 0
    self.bet = 0
    self.turns = 0

  def show_hand(self):
    count = 1
    print("\n{} holding -".format(self.name))
    for hand in self.hands:
      print("{} cards in Hand {}:".format(str(hand.count), count))
      for key, value in hand.cards.items():
        for card in value:
          print(card)
      print("\n")
      count += 1

  def get_name(self):
    return self.name

  def __str__(self):
    playerString = ""
    playerString += "PLAYER {}\nName: {}\nCash: {}\nBet: {}\nHands: {}\n".format(self.num, self.name, self.cash, self.bet, len(self.hands))
    count = 1

    for hand in self.hands:
      playerString += "Hand {} value: {}\n".format(count, hand.value)
      count += 1
    return playerString

# Dealer subcalass of Player with special features
class Dealer(Player):

  def __init__(self, name, num):
    Player.__init__(self, name, num)

  def deal_card(self, hand, deck):
    card = deck.pop_card()

    if(card.title != "Ace"):
      cardType = "fixedCards"
    else:
      cardType = "aces"

    # add card to Hand, update hand stats, assign bust or not
    hand.cards[cardType].append(card)
    hand.recalculate_value()
    hand.check_hand()

    # print("{} - removed from deck and dealt to {}".format(card, player.name))

class Hand():
  def __init__(self):
      self.cards = {'fixedCards':[], 'aces': []}
      self.value = 0
      self.count = 0
      self.state = ""
      self.num = 1
      self.playable = True

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

    self.count = len(self.cards['fixedCards']) + len(self.cards['aces'])

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
    
  # check if hand is bust or blackjack (loss/win), don't like code dupe
  def check_hand(self):
    if(self.value == 21):
      self.state = 'Blackjack'
      self.playable = False
    elif self.value > 21:
      self.state = 'Bust'
      self.playable = False
    else:
      self.state = 'Active'
            
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
    # adding attributes for potential art to be added
    # art for Front,Back, pos for x,y
    self.art = [None, None]
    self.pos = [None, None]

  # print card in correct format
  def __str__(self):
    return "{} of {} - ({})".format(self.title, self.suit, self.value)

class Option():

  def __init__(self, num, name, method):
    self.num = num
    self.name = name
    self.method = method

  def __str__(self):
    return "{}. {}".format(self.num, self.name)

class Game():
  def __init__(self):
    self.players = None
    self.dealer = None
    self.deck = None
    self.play = True
    self.buyIn = 0
    self.multi = True
    self.bets = {}
    self.options = []

  def setup(self):
    # welcome message and Player creation
    print("Welcome to Python Blackjack, also known as Twenty One!")

    # Players
    self.players = self.create_players()

    # Deck
    self.deck = self.create_deck()

    # Dealer
    self.dealer = Dealer("Dealer", 0)

    # Buy in
    self.assign_cash()

    # Bet tracker
    self.bet_tracker_setup()

  def generate_options(self, hand):
    stand = Option(1, "Stand", self.stand)
    hit = Option(2, "Hit", self.hit)
    double = Option(3, "Double", self.double)
    split = Option(4, "Split", self.split)
    surrender = Option(5, "Surrender", self.surrender)

    # check for same value cards for split option to be added or removed
    #for cardType in hand.cards:
    #  for card in cardType:
    #    pass

    # update options
    self.options = [stand, hit, double, split, surrender]

  def select_option(self, num):
    print("HERE")
    for option in self.options:
      print("HERE2")
      if(option.num == num):
        print("{} selected".format(option.name))

  def initial_deal(self):
    # deal two cards into Hand 1, all Players start with 1 Hand (0)
    for x in range(0,2):
      for player in self.players:
        for hand in player.hands:
          self.dealer.deal_card(hand, self.deck)
      # deal Dealer, too
      for hand in self.dealer.hands:
        self.dealer.deal_card(hand, self.deck)

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
    self.buyIn = cash

  def create_players(self):
    players = ()
    num = 0

    # multiplayer if game.multi = True
    if(self.multi == True):
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
      players += (Player(name, x),)

    return players

  def bet_tracker_setup(self):
    # bet tracker dictionary for all players {'Player x' : value}
    for player in self.players:
      self.bets['Player '+str(player.num)] = 0

  def create_deck(self):
    deck = Deck()
    deck.build()
    deck.shuffle()

    return deck

# Player passes and holds Hand as is
  def stand(self, player):
    print("{} stands with his/her cards.".format(player.name))

# Player requests extra card
  def hit(self, hand):
    self.dealer.deal_card(hand, self.deck)

# if Player has enough cash to double bet, double bet and
# set state double to True
  def double(self, player, hand):
    if(player.bet <= player.cash):
      player.cash -= player.bet
      player.bet *= 2
      player.states['Double'] = True
      this.bets['Player {}'.format(player.num)] += player.bet

      # deal card
      self.dealer.deal_card(hand, self.deck)

      return True
    else:
      return False

  # if Player has double cards, pass in Hand with doubles
  # allow split to add new hand and deal extra card to
  # each Hand. handInfo is {num: x, cardType: x}
  def split(self, player, hand):
    newHand = Hand()
    
    # assign Hand number
    newHand.num = len(player.hands + 1)

    # check for card type
    if(len(hand.cards['fixedCards']) == 2):
      cardType = 'fixedCards'
    else:
      cardType = 'aces'

    # pop card off appropriate array in Hand
    card = hand.cards[cardType].pop()

    # put card into new Hand
    newHand.cards[cardType].append(card)

    # deal a new card to each Hand
    self.dealer.deal_card(hand, self.deck)
    self.dealer.deal_card(newHand, self.deck)
   
    # add Hand to player's hands
    player.hands += (newHand, )

    return None

  # forfeit half of bet and drop out, only possible on first two cards
  def surrender(self, player):
    player.bet /= 2
    player.cash += player.bet
    player.playing = False
    print("{} surrenders and takes back half their wager of {}".format(player.name, player.bet))

  def print_options(self):
    for option in self.options:
      print(option)

  def select_option(self, num):
    return None

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

  def print_bet_tracker(self):
    print("BET TRACKER:")
    for key, value in self.bets.items():
      print("{}: ${}\n".format(key, value))

  def show_players_hands(self):
    for player in self.players:
      player.show_hand()
    self.dealer.show_hand()