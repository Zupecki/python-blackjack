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

# deal 2 cards to each player, including dealer

game.initial_deal()

# Game loop
while game.play != False:
	for player in game.players:
		for hand in player.hands:
			print("Player {} ({}) - what would you like to do with Hand {}?".format(player.num, player.name, hand.num))
			game.generate_options(hand)
			game.print_options()
			game.select_option(input())


# print player hand states
for player in game.players:
	count = 1
	print("{}'s Hand states are:\n".format(player.name))
	for hand in player.hands:
	  print("Hand {}: {}".format(count, hand.state))
	  count += 1

# Player enters name - how many players? **kwargs? (["Michael": 1, "Jason": 2"]) etc? Or **args? (["Michael, Jason"]) etc?
# Cards created
# Cards shuffled
# Cards dealt
# Continue to calculate hand for every Card dealt
# If either exceeds 21, other Player wins
# If either Player or Dealer hit 21, they win. Dealer wins if both are 21

##
