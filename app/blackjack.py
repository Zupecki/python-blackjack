# Initial primary code for command line Blackjack - might split into separate files if necessary
# A Game has Players, a Dealer and a Deck of Cards
# A Player has Cards and set of actions
# A Deck has Cards or is Empty
import sys
import random
sys.path.append('..')

import src.classes as blackjack

# Game logic

# Build game object, then set it up with Players, Dealer and Deck

game = blackjack.Game()
game.setup()
#print("\n")

# show Deck for testing

game.deck.show_cards()
print("\n{} cards in the deck.\n".format(game.deck.count))

# deal 2 cards to each player, including dealer

game.initial_deal()

# show hand

game.show_players_hands()

# report how many cards are in the deck

print("\n{} cards in the deck.\n".format(game.deck.count))

# print players

game.print_players()

# split player 1's hand
game.split(game.players[0])

# show hands again

game.show_players_hands()

# print players again

game.print_players()

# print bet tracker

game.print_bet_tracker()

# print player state

for player in game.players:
  print("{} busted is {}".format(player.name, player.states['Bust']))
  print("{} blackjack is {}".format(player.name, player.states['Blackjack']))

# Player enters name - how many players? **kwargs? (["Michael": 1, "Jason": 2"]) etc? Or **args? (["Michael, Jason"]) etc?
# Cards created
# Cards shuffled
# Cards dealt
# Continue to calculate hand for every Card dealt
# If either exceeds 21, other Player wins
# If either Player or Dealer hit 21, they win. Dealer wins if both are 21

##
