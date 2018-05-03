# Initial primary code for command line Blackjack - might split into separate files if necessary
# A Game has Players, a Dealer and a Deck of Cards
# A Player has Cards and set of actions
# A Deck has Cards or is Empty
from random import shuffle
from inspect import getargspec as argnames

# misc global functions - probably best in own file

# convert int num to word-string version
def num_to_word(num):
  ref = {0:"Zero",1:"One",2:"Two",3:"Three",4:"Four",5:"Five",
  6:"Six",7:"Seven",8:"Eight",9:"Nine",10:"Ten"}

  return ref[num]

def num_range_input_validation(inputType, minimum, maximum, intentMessage, rangeMessage):

  while True:
      try:
        num = inputType(input())
      except ValueError:
        print("Must be a number, try again.\n{}".format(intentMessage))
        continue
      else:
        if(num >= minimum and num <= maximum):
          break
        else:
          print("Sorry, {}.\n{}".format(rangeMessage, intentMessage))
          continue

  return num

# return tuple of just the argument names, discluding 'self' // redundant code, leaving for record
def get_arg_names(function):
  # pull arg names as index 0, drop 'self' with slice, cast to tuple
  return tuple(argnames(function)[0][1:])

class Player():

  def __init__(self, name, num):
    self.num = num
    self.name = name
    self.hands = (Hand(), )
    self.state = {'Active': True, 'Context': 'Active'}
    self.cash = 0
    self.bet = 0
    self.turns = 0

  def show_hand(self, hand):

    for card in hand.cards['allCards']:
      if(card.faceUp == True):
        print(card)
      else:
        print("Face Down - ?")

  # Player turns are over, check state and set validity for potential payouts
  def end_state(self):
    context = ""
    busts = 0

    # check hands to see if any are valid, count busts
    for hand in self.hands:
      if hand.state['Context'] != 'Bust':
        context = "Valid"
        break
      else:
        busts += 1
    
    # if Player surrendered, or all hands are Bust, set to invalid
    if(self.state['Context'] == 'Surrendered' or len(self.hands) == busts):
      context = "Invalid"

    self.set_state(False, context)

  def get_name(self):
    return self.name

  def set_state(self, active, context):
    self.state['Active'] = active
    self.state['Context'] = context

  def __str__(self):
    playerString = ""
    playerString += "PLAYER {}\nName: {}\nCash: {}\nBet: {}\nHands: {}\nActive: {}\n".format(self.num, self.name, self.cash, self.bet, len(self.hands), self.state['Active'])

    for hand in self.hands:
      playerString += "Hand {} value: {}\n".format(hand.num, hand.value)
    return playerString

# Dealer subcalass of Player with special features
class Dealer(Player):

  def __init__(self, name, num):
    Player.__init__(self, name, num)

  def deal_card(self, player, hand, deck, dealStyle):
    card = deck.pop_card()

    # check the deal style, default is London
    if(dealStyle == 'Nevada'):
      card.faceUp = False
    elif(dealStyle == 'London'):
      card.faceUp = True
    elif(dealStyle == 'Dealer'): # Dealer's cards always face down, then one can be flipped
      card.faceUp = False

    # append all cards to allCards list
    hand.cards['allCards'].append(card)

    # if Ace add same card into aces list too for easy manipulation
    # same card exists in two places
    if(card.title == "Ace"):
      hand.cards['aces'].append(card)

    # Update hand stats, assign bust or not
    hand.recalculate_value()
    hand.check_hand()

    # print("{} - removed from deck and dealt to {}".format(card, player.name))

class Hand():
  def __init__(self):
      self.cards = {'allCards':[], 'aces': []}
      self.value = 0
      self.count = 0
      self.state = {'Active': True, 'Context': 'Playable'}
      self.num = 1
      self.soft = True

  # iterate through all cards and sum hand value
  def recalculate_value(self):
    self.value = 0

    # sum value of cards
    for card in self.cards['allCards']:
      self.value += card.value

    # if hand value over 21, and there is at least one ace, else bust!
    if self.value > 21 and len(self.cards['aces']) > 0:
      self.change_aces()

    self.count = len(self.cards['allCards']) + len(self.cards['aces'])

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
    
  # Check if hand is Blackjack or Bust, otherwise leave untouched
  def check_hand(self):
    if(self.value == 21):
      self.set_state(False, 'Blackjack')
    elif self.value > 21:
      self.set_state(False, 'Bust')

  def set_state(self, active, context):
    self.state['Active'] = active
    self.state['Context'] = context
            
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
    self.faceUp = True
    # adding attributes for potential art to be added
    # art for Front,Back, pos for x,y
    self.art = [None, None]
    self.pos = [None, None]

  def flip_card(self):
    self.faceUp = not self.faceUp

  # print card in correct format
  def __str__(self):
    return "{} of {} - ({})".format(self.title, self.suit, self.value)

class Option():

  def __init__(self, name, method):
    self.num = 0
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
    self.multi = True
    self.bets = {}
    self.options = []
    self.minBet = 0
    self.dealStyle = 'London'
    self.playerRound = True

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
    stand = Option("Stand", self.stand)
    hit = Option("Hit", self.hit)
    double = Option("Double", self.double)
    split = Option("Split", self.split)
    surrender = Option("Surrender", self.surrender)

    useSplit = False

    # update options
    self.options = [stand, hit]

    # check if first two cards for double
    if(len(hand.cards['allCards']) == 2):
      self.options.append(double)
      # check for same value cards on intial deal for split option
      for card in hand.cards['allCards']:
        cardVal = card.value
        for compareCard in hand.cards['allCards']:
          if(card != compareCard and cardVal == compareCard.value):
            useSplit = True
            break

    if(useSplit == True):
       self.options.append(split)

    # add surrender to end
    self.options.append(surrender)

    # generate nums for options
    for x in range(0,len(self.options)):
      self.options[x].num = x+1

  def dealer_hit(self):
    hand = self.dealer.hands[0]

    # flip face down card
    hand.cards['allCards'][1].flip_card()

    while(hand.value < 17 and hand.soft == True):
      self.dealer.deal_card(self.dealer, hand, self.deck, self.dealStyle)

    # check for soft 17
    # if(len(hand['aces']) > 0):


  def menu_select(self, num):
    for option in self.options:
      if(option.num == int(num)):
        #print("{} selected from options menu.".format(option.name))
        return option.method
        
  def select_option(self):
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
          self.dealer.deal_card(player, hand, self.deck, self.dealStyle)
      # deal Dealer, too
      for hand in self.dealer.hands:
        self.dealer.deal_card(player, hand, self.deck, 'Dealer')

    # flip one Dealer Card
    self.dealer.hands[0].cards['allCards'][0].flip_card()

  def assign_cash(self):
    print("How much cash does each Player start with? ($100-$1000)")

    cash = num_range_input_validation(int, 100, 1000, "How much cash does each Player start with?", "cash can only be between $100 and $1000")

    for player in self.players:
      player.cash = cash

    self.dealer.cash = cash

    print("What is to be the minimum bet for the game? ($1-$1000)")
    minBet = num_range_input_validation(int, 1, 1000, "What is the minimum bet for the game?", "min bet must be between $1 and $1000")
    self.minBet = minBet

  def create_players(self):
    players = ()
    num = 0

    # multiplayer if game.multi = True, else 1 Player
    if(self.multi == True):
      print("How many players?")

      # validate that input is a number by casting to int and capturing exception
      num = num_range_input_validation(int, 1, 7, "How many Players?", "game can only be between 1 and 7 Players")
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
      self.bets['Player '+str(player.num)] = player.bet # THIS DOESN'T WORK?

  def collect_bets(self):
    for player in self.players:
      if(player.cash >= self.minBet):
        print("Player {} ({}), what is your bet? (Must be at least {})\nCash balance: ${}".format(player.num, player.name, self.minBet, player.cash))
        bet = num_range_input_validation(int, self.minBet, player.cash, "What is your bet? (Must be at least {})".format(self.minBet), "bet must be between {} and your cash ({})".format(self.minBet, player.cash))
        # take bet away from cash and add to game.bets and player.bet
        self.bets['Player {}'.format(player.num)] = bet
        player.bet = bet
        player.cash -= bet
      else: # has less than games min bet, broke
        print("Sorry Player {} ({}), you're broke and can't play!".format(player.num, player.name))
        player.set_state(False, 'Broke')

  def process_results(self):
    results = {'Winners':[], 'Losers':[], 'Ties':[]}

    if(self.dealer.state['Context'] == 'Invalid'):
    # if dealer bust, pay out everyone with valid hands
      for player in self.players:
        if(player.state['Context'] == 'Valid'):
          results['Winners'].append(player)
        else:
          results['Losers'].append(player)

    # else dealer not bust, compare hands
    else:
      dealerHand = self.dealer.hands[0].value
      for player in self.players:
        playerHandStates = {'Wins': 0, 'Ties': 0, 'Losses': 0}
        if(player.state['Context'] != 'Bust'):
          playerHandCount = len(player.hands)
          for hand in player.hands:
            if(hand.state['Context'] != 'Bust'):
              if(hand.value > dealerHand):
                playerHandStates['Wins'] += 1
              elif(hand.value == dealerHand):
                playerHandStates['Ties'] += 1
              elif(hand.value < dealerHand):
                playerHandStates['Losses'] += 1
        else:
          results['Losers'].append(player)

        if(playerHandStates['Wins'] > 0):
          results['Winners'].append(player)
          break
        elif(playerHandStates['Ties'] > 0):
          results['Ties'].append(player)
          break
        else:
          results['Losers'].append(player)

    # print results
    for player in results['Winners']:
      player.cash += player.bet*2
      print("Congratulations Player {} ({}), you beat the dealer and won ${}!".format(player.num, player.name, player.bet*2))
      print("You now have ${}!".format(player.cash))

    for player in results['Ties']:
      player.cash += player.bet
      print("Player {} ({}), you tied with the dealer and receive your ${} back!".format(player.num, player.name, player.bet*2))
      print("You now have ${}!".format(player.cash))

    for player in results['Losers']:
      print("Sorry Player {} ({}), you were beaten by the dealer and lost ${}!".format(player.num, player.name, player.bet))

    # print Dealer final state for test purposes
    print("Dealer states:\nDealer Active - {}\nDealer Context - {}\nHand Active - {}\nHand Context - {}\n".format(self.dealer.state['Active'], self.dealer.state['Context'], self.dealer.hands[0].state['Active'], self.dealer.hands[0].state['Context']))

  def create_deck(self):
    deck = Deck()
    deck.build()
    deck.shuffle()

    return deck

# Player passes and holds Hand as is
  def stand(self, player, hand):
    print("{} stands with his/her cards on Hand {}.".format(player.name, hand.num))

    hand.set_state(False, 'Stand')

# Player requests extra card
  def hit(self, player, hand):
    print("{} hits and receives a new card for Hand {}.".format(player.name, hand.num))
    self.dealer.deal_card(player, hand, self.deck, self.dealStyle)

# if Player has enough cash to double bet, double bet and
# set state double to True
  def double(self, player, hand):
    if(player.bet <= player.cash):
      player.cash -= player.bet
      player.bet *= 2

      print("{} doubles their bet to {} and receives a new card for Hand {}.".format(player.name, player.bet, hand.num))

      # change player state
      hand.set_state(False, 'Double')

      # double bet in bet tracker
      self.bets['Player {}'.format(player.num)] = player.bet

      # deal card
      self.dealer.deal_card(player, hand, self.deck, self.dealStyle)

  # if Player has double cards, pass in Hand with doubles
  # allow split to add new hand and deal extra card to each Hand
  def split(self, player, hand):
    newHand = Hand()
    
    # assign Hand number - current amount +1
    newHand.num = len(player.hands) + 1

    # print output
    print("{} splits their hands and receives a new card for Hand {} and Hand {}.".format(player.name, hand.num, newHand.num))

    # check for card type
    if(len(hand.cards['allCards']) == 2):
      cardType = 'allCards'
    else:
      cardType = 'aces'

    # pop card off appropriate array in Hand
    card = hand.cards[cardType].pop()

    # put card into new Hand
    newHand.cards[cardType].append(card)

    # deal a new card to each Hand
    self.dealer.deal_card(player, hand, self.deck, self.dealStyle)
    self.dealer.deal_card(player, newHand, self.deck, self.dealStyle)
   
    # add Hand to player's hands
    player.hands += (newHand, )

  # forfeit half of bet and drop out, only possible on first two cards
  def surrender(self, player, hand):
    player.bet /= 2
    player.cash += player.bet

    player.set_state(False, 'Surrendered')

    print("{} surrenders Hand {} and takes back half their wager of {}, totalling {}.".format(player.name, hand.num, player.bet*2, player.bet))

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

  def check_players_money(self):
    for player in self.players:
      if(player.cash >= self.minBet):
        return True
    print("Sorry, no one has enough money to buy in for the minimum ${} bet, game over!".format(self.minBet))
    return False
  
  def reset(self):
    # wipe Player bets to 0, empty Hands, reset states
    for player in self.players:
      player.bet = 0
      player.hands = (Hand(), )
      player.state = {'Active': True, 'Context': 'Active'}

    # create new deck
    self.deck = self.create_deck()

    # empty Dealer Hands
    self.dealer.hands = (Hand(), )

    # reset playerRound boolean
    self.playerRound = True

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