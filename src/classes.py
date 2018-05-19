# Initial primary code for command line Blackjack - might split into separate files if necessary
# A Game has Players, a Dealer and a Deck of Cards
# A Player has Cards and set of actions
# A Deck has Cards or is Empty
from random import shuffle
from inspect import getargspec as argnames
from time import time, sleep
import sys
import os

# misc global functions - probably best in own file

# convert int num to word-string version
def num_to_word(num):
  ref = {0:"Zero",1:"One",2:"Two",3:"Three",4:"Four",5:"Five",
  6:"Six",7:"Seven",8:"Eight",9:"Nine",10:"Ten"}

  return ref[num]

def print_slow_and_wait(inputString, printDelay, wait):
  printString = ""

  for char in inputString:
    printString += char
    sys.stdout.write(printString+"\r")
    sys.stdout.flush()
    sleep(printDelay)
  print("")

  sleep(wait)

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

# wipe console
def wipe_console():
  print("\033[H\033[J")

class Player():

  def __init__(self, name, num):
    self.num = num
    self.name = name
    self.hands = (Hand(), )
    self.state = {'Active': True, 'Context': 'Active'}
    self.cash = 0
    self.bet = 0
    self.turns = 0
    self.bestHand = 0

  def show_hand(self, hand):

    for card in hand.cards['allCards']:
      if(card.faceUp == True):
        print(card)
      else:
        print("Face Down - ?")

  # Player turns are over, check state and set validity for potential payouts
  def end_state(self, game):
    context = ""
    busts = 0

    # if Surrendered, leave as is, else hoist best Hand state to Player state
    if(self.state['Context'] != 'Surrendered'):

      # check hands to see if any are valid, count busts
      for hand in self.hands:
        if(hand.state['Context'] == 'Blackjack'):
          context = "Blackjack"
          game.lastAction = "Player {} ({}) hit BLACKJACK!".format(self.num, self.name)
          print_slow_and_wait("Congratulations {} - BLACKJACK!".format(self.name), 0.06, 2)
          break
        elif(hand.state['Context'] != 'Bust'):
          context = "Open"
          break
        else:
          busts += 1
      
      # if Player's hands are Bust, set to Bust
      if(len(self.hands) == busts):
        context = "Bust"
        game.lastAction = "Player {} ({}) is BUST!".format(self.num, self.name)
        print_slow_and_wait("BUSTED!", 0.06, 2)

      self.set_state(False, context)

  def get_name(self):
    return self.name

  def get_num(self):
    return self.num

  def get_hands(self):
    return self.hands

  def set_state(self, active, context):
    self.state['Active'] = active
    self.state['Context'] = context

  def best_hand(self):
    # iterate through all hands, find best valid hand
    for hand in self.hands:
      if(self.state['Context'] == 'Bust'):
        if(hand.value < self.bestHand or self.bestHand == 0):
          self.bestHand = hand.value
      else:
        if(hand.value > self.bestHand):
          self.bestHand = hand.value

  def __str__(self):
    playerString = ""
    playerString += "PLAYER {}\nName: {}\nCash: {}\nBet: {}\nHands: {}\nActive: {}\nContext: {}\n".format(self.num, self.name, self.cash, self.bet, len(self.hands), self.state['Active'], self.state['Context'])

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
    hand.check_hand(player)

    return card

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
  def check_hand(self, player):
    if(self.value == 21):
      #print_slow_and_wait("Congratulations Player {} ({}) - you hit Blackjack!".format(player.num, player.name), 0.06, 2)
      self.set_state(False, 'Blackjack')
    elif self.value > 21:
      self.set_state(False, 'Bust')

  def set_state(self, active, context):
    self.state['Active'] = active
    self.state['Context'] = context

  def get_value(self):
    for card in self.cards['allCards']:
      if(card.faceUp == False):
        return "?"
    return self.value

  def get_num(self):
    return self.num
            
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

  def get_string(self):
    if(self.faceUp == True):
      return "{} of {} - ({})".format(self.title, self.suit, self.value)
    else:
      return "Face Down - ?"

  # print card in correct format
  def __str__(self):
    if(self.faceUp == True):
      return "{} of {} - ({})".format(self.title, self.suit, self.value)
    else:
      return "Face Down - ?"

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
    self.minBet = 0
    self.dealStyle = 'London'
    self.playerRound = True
    self.roundCount = 1
    self.lastAction = ""
    self.allBust = True

  def setup(self):
    # welcome message and Player creation
    print_slow_and_wait("Welcome to Python Blackjack in the command line!", 0.06, 1)

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
    options = []
    stand = Option("Stand", self.stand)
    hit = Option("Hit", self.hit)
    double = Option("Double", self.double)
    split = Option("Split", self.split)
    surrender = Option("Surrender", self.surrender)

    useSplit = False

    # update options
    options = [stand, hit]

    # check if first two cards for double
    if(len(hand.cards['allCards']) == 2):
      options.append(double)
      # check for same value cards on intial deal for split option
      for card in hand.cards['allCards']:
        cardVal = card.value
        for compareCard in hand.cards['allCards']:
          if(card != compareCard and cardVal == compareCard.value):
            useSplit = True
            break

    if(useSplit == True):
      options.append(split)

    # add surrender to end
    options.append(surrender)

    # generate nums for options
    for x in range(0,len(options)):
      options[x].num = x+1

    return options

  def dealer_hit(self):
    hand = self.dealer.hands[0]

    # flip face down card
    hand.cards['allCards'][1].flip_card()

    # wipe console and print title
    wipe_console()
    self.print_title()

    print("DEALERS TURN:\n")
    print_slow_and_wait("Dealer flips second card and shows hand...", 0.06, 2)

    # show cards
    for card in hand.cards['allCards']:
      print_slow_and_wait(card.get_string(), 0, 1)

    while(hand.value < 17 and hand.soft == True):
      card = self.dealer.deal_card(self.dealer, hand, self.deck, self.dealStyle)
      print_slow_and_wait("Dealer hits and receives {}".format(card), 0.06, 1)

  def menu_select(self, num, options):
    for option in options:
      if(option.num == int(num)):
        #print("{} selected from options menu.".format(option.name))
        return option.method

  def check_all_bust(self):
    for player in self.players:
      if(player.state['Context'] != 'Bust'):
        self.allBust = False

  def initial_deal(self):
    # deal two cards into Hand 1, all Players start with 1 Hand (0)
    for x in range(0,2):
      for player in self.players:
        if(player.state['Active'] == True):
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

    # assign players to Game object
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

    # pull best hand value for each Player
    for player in self.players:
      player.best_hand()

    # if dealer bust, pay out everyone with valid hands
    if(self.dealer.state['Context'] == 'Bust'):
      for player in self.players:
        if(player.state['Context'] == 'Open' or player.state['Context'] == 'Blackjack'):
          results['Winners'].append(player)
        else: # Bust or Surrendered
          results['Losers'].append(player)

    # else dealer not bust, compare hands
    else:
      dealerHandValue = self.dealer.hands[0].value

      for player in self.players:
        # if Player has Blackjack
        if(player.state['Context'] == 'Blackjack'):
          if(dealerHandValue < 21):
            results['Winners'].append(player)
          else:
            results['Ties'].append(player)

        # if Player not Bust, Surrendered or Blackjack, compare to dealer
        elif(player.state['Context'] == 'Open'):
          # compare best hand to dealer hand and assign player to appropriate list
          if(player.bestHand > dealerHandValue):
            results['Winners'].append(player)
          elif(player.bestHand == dealerHandValue):
            results['Ties'].append(player)
          elif(player.bestHand < dealerHandValue):
            results['Losers'].append(player)
       
        # straight up losers
        elif(player.state['Context'] == 'Bust' or player.state['Context'] == 'Surrendered'):
          results['Losers'].append(player)

    return results

  def print_results(self, results):
    # wipe console and print title
    wipe_console()
    self.print_title()

    print_slow_and_wait("ROUND RESULTS:", 0, 0)
    print_slow_and_wait("Dealer's final hand -", 0, 0)
    print_slow_and_wait("Value: {}".format(self.dealer.hands[0].value), 0, 1)

    # print Winners
    for player in results['Winners']:
      winnings = 0
      if(player.state['Context'] == 'Open'):
        winnings = player.bet #regular win
      elif(player.state['Context'] == 'Blackjack'):
        winnings = player.bet*1.5 #blackjack win

      # update Player cash
      player.cash += (player.bet + winnings)

      # print
      print("")
      print_slow_and_wait("Congratulations Player {} ({}), you beat the dealer!".format(player.num, player.name), 0, 0)
      print_slow_and_wait("Hand value: {}".format(player.bestHand), 0, 0)
      print_slow_and_wait("Winnings: ${}".format(winnings), 0, 0)
      print_slow_and_wait("You now have ${}!".format(player.cash), 0, 1)

    # print Ties
    for player in results['Ties']:
      player.cash += player.bet

      # print
      print("")
      print_slow_and_wait("Player {} ({}), you tied with the dealer!".format(player.num, player.name), 0, 0)
      print_slow_and_wait("Tied hand value: {}".format(player.bestHand), 0, 0)
      print_slow_and_wait("You receive back your bet of ${}".format(player.bet), 0, 0)
      print_slow_and_wait("You now have ${}!".format(player.cash), 0, 1)

    # print Losers
    for player in results['Losers']:
      message = ""
      losses = 0
      if(player.state['Context'] == 'Bust'):
        message = "Bust"
        losses = player.bet
      elif(player.state['Context'] == 'Surrendered'):
        message = "Surrendered"
        losses = player.bet/2
      elif(player.state['Context'] == 'Open'):
        message = "Lower Hand Value"
        losses = player.bet

      # print
      print("")
      print_slow_and_wait("Sorry Player {} ({}), you were beaten by the dealer!".format(player.num, player.name), 0, 0)
      print_slow_and_wait("Reason for loss: {}".format(message), 0, 0)
      print_slow_and_wait("Hand value: {}".format(player.bestHand), 0, 0)
      print_slow_and_wait("You lost ${}!".format(player.bet), 0, 0)
      print_slow_and_wait("You now have ${}!".format(player.cash), 0, 1)

  def create_deck(self):
    deck = Deck()
    deck.build()
    deck.shuffle()

    return deck

# Player passes and holds Hand as is
  def stand(self, player, hand):
    message = "{} stands with their cards on Hand {}.".format(player.name, hand.num)
    print_slow_and_wait(message, 0.03, 2)

    hand.set_state(False, 'Stand')

    # update last action
    self.lastAction = message

# Player requests extra card
  def hit(self, player, hand):
    # deal card
    card = self.dealer.deal_card(player, hand, self.deck, self.dealStyle)

    # print output
    message = "{} hits and receives {} for Hand {}.".format(player.name, card, hand.num)
    print_slow_and_wait(message, 0.03, 2)

    # update last action
    self.lastAction = message

# if Player has enough cash to double bet, double bet and
# set state double to True
  def double(self, player, hand):
    if(player.bet <= player.cash):
      player.cash -= player.bet
      player.bet *= 2

      # change player state
      hand.set_state(False, 'Double')

      # double bet in bet tracker
      self.bets['Player {}'.format(player.num)] = player.bet

      # deal card
      card = self.dealer.deal_card(player, hand, self.deck, self.dealStyle)

      # print output
      message = "{} doubles their bet to {} and receives {} for Hand {}.".format(player.name, player.bet, card, hand.num)
      print_slow_and_wait(message, 0.03, 2)

      # update last action
      self.lastAction = message


  # if Player has double cards, pass in Hand with doubles
  # allow split to add new hand and deal extra card to each Hand
  def split(self, player, hand):
    newHand = Hand()
    
    # assign Hand number - current amount +1
    newHand.num = len(player.hands) + 1

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
    cardOne = self.dealer.deal_card(player, hand, self.deck, self.dealStyle)
    cardTwo = self.dealer.deal_card(player, newHand, self.deck, self.dealStyle)
   
    # add Hand to player's hands
    player.hands += (newHand, )

    # print output
    message = "{} splits their hands and receives {} for Hand {} and {} for Hand {}.".format(player.name, cardOne, hand.num, cardTwo, newHand.num)
    print_slow_and_wait(message, 0.03, 2)

    # update last action
    self.lastAction = message

  # forfeit half of bet and drop out, only possible on first two cards
  def surrender(self, player, hand):
    # print output
    message = "{} surrenders and loses ${} of their ${} bet.".format(player.name, int(player.bet/2), player.bet)
    print_slow_and_wait(message, 0.03, 2)

    # update last action
    self.lastAction = message

    # edit bet and cash
    player.bet /= 2
    player.cash += player.bet

    # set states
    player.set_state(False, 'Surrendered')
    hand.set_state(False, 'Surrendered')

  def print_options(self, options, player, hand):
    playerName = player.name
    handNum = hand.num

    print("OPTIONS:\n")
    for option in options:
      print(option)

    print("\n{}, what would you like to do with Hand {}?".format(playerName, handNum))

  def end(self):
    print("\nWould you like to play another round, Y/N?")

    while True:
      choice = input().upper()

      if(choice == 'Y' or choice == 'N'):
        if(choice == 'Y'):
          self.reset()
          break
        elif(choice == 'N'):
          self.play = False
          break
      else:
        print("Sorry, must be Y or N, try again.")
        continue

  def check_players_money(self):
    play = False
    for player in self.players:
      if(player.cash >= self.minBet):
        play = True
      else:
        player.state['Active'] = False
        player.state['Context'] = 'Poor'

    if(play):
      return True
    else:
      print("Sorry, no one has enough money to buy in for the minimum ${} bet, game over!".format(self.minBet))
      return False
  
  def reset(self):
    # wipe console
    zeroHold = os.system("clear")

    # wipe Player bets to 0, empty Hands, reset states
    for player in self.players:
      player.bet = 0
      player.hands = (Hand(), )
      player.state = {'Active': True, 'Context': 'Active'}
      player.bestHand = 0

    # create new deck
    self.deck = self.create_deck()

    # empty Dealer Hands
    self.dealer.hands = (Hand(), )

    # reset playerRound boolean
    self.playerRound = True

    # increment round counter
    self.roundCount += 1

    # wipe last action
    self.lastAction = ""

    # reset all bust to True (turns False before Dealer's turn, if at least one Player isn't Bust)
    self.allBust = True

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

  def print_title(self):
    # print Title
    print("Python Blackjack - Round {}\n".format(self.roundCount))
    print("----------------------------------------------------")

  def render_turn(self, player, playerHand):
    # wipe console and print title
    wipe_console()
    self.print_title()

    # fetch round format
    render = self.round_format(player, playerHand)

    # PRINT IT
    for x in range(0, len(render[0])):
      if(render[1][x] == None):
        print(render[0][x])
      else:
        spaces = self.calc_spaces(render[0][x])
        print(render[0][x]+spaces+render[1][x])

  def round_format(self, player, playerHand):
    dealerHand = self.dealer.hands[0]
    playerNum = player.get_num()
    playerName = player.get_name()
    handValue = playerHand.get_value()
    handNum = playerHand.get_num()
    stateStrings = [[],[]] # column 1, column 2

  
    stateStrings[0].append("LAST ACTION:")
    stateStrings[1].append(None)

    if(len(self.lastAction) > 0):
      stateStrings[0].append("{}".format(self.lastAction))
    else:
      stateStrings[0].append("New Round")
    stateStrings[1].append(None)

    stateStrings[0].append("----------------------------------------------------")
    stateStrings[1].append(None)

    stateStrings[0].append("PLAYER {} of {}:\n".format(playerNum, len(self.players)))
    stateStrings[1].append(None)

    stateStrings[0].append("Name: {}".format(playerName))
    stateStrings[1].append("Cash: {}".format(player.cash))

    stateStrings[0].append("Hands: {}".format(len(player.hands)))
    stateStrings[1].append("Bet: {}".format(player.bet))

    stateStrings[0].append("----------------------------------------------------")
    stateStrings[1].append(None)
    
    stateStrings[0].append("HANDS:\n")
    stateStrings[1].append(None)

    stateStrings[0].append("Dealer's Hand -")
    stateStrings[1].append("Your Hand {} of {} -".format(handNum, len(player.hands)))

    stateStrings[0].append("Value: {}".format(dealerHand.get_value()))
    stateStrings[1].append("Value: {}".format(handValue))

    # FORMAT CARD STRING ROWS
    rowCount = 0

    # calculate card rows needed based on Player cards (Dealer always has only 2 Cards)
    rowCount = len(playerHand.cards['allCards'])

    # add card strings to array
    for x in range(0, rowCount):
      if(x < 2): # add Dealer card if rows less than 3
        stateStrings[0].append(dealerHand.cards['allCards'][x].get_string())
      else:
        stateStrings[0].append("")

      # always add Player Cards
      stateStrings[1].append(playerHand.cards['allCards'][x].get_string())

    stateStrings[0].append("----------------------------------------------------")
    stateStrings[1].append(None)

    return stateStrings

  def calc_spaces(self, stringInput):
    string = ""
    for x in range(len(stringInput), 29):
      string += " "
    return string