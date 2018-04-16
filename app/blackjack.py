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

# Betting round
game.collect_bets()

# deal 2 cards to each player, including dealer
game.initial_deal()

# Game loop
while game.play != False:
	for player in game.players:
		if(player.state['Active'] == True):
			# print Player details here - name, cash, hand info?
			for hand in player.hands:
				print("\nPlayer {} ({}) - what would you like to do with Hand {}?".format(player.num, player.name, hand.num))
				player.show_hand(hand)
				game.generate_options(hand)
				game.print_options()

				choice = input()

				option = game.menu_select(choice) # return correct option method

				optionArgs = blackjack.get_arg_names(option)

				option(eval(*optionArgs)) # sometimes requires player and hand, need solution
				# doesn't work for multiple arguments, although solves for hit and stand and surrender
				
				#print("ARGS")
				#print(blackjack.get_arg_names(option))

			# after Player has acted on all Hands, check if still in the game
			player.check_active()
		else:
			print("Sorry Player {} ({}), you only have ${} and the minimum bet is $100")

	# bail out of game
	game.play = False

	# dealer behaviour - keep hitting until between 17 and 21
	# check if anyone has hit Blackjack and announce winners
	# pay out results, flush bet tracker

	# change Hand class to only have complete list of ALL cards, and one for Aces (duplicate instances), this will simplify some code
	# should there be a player_turn function to take in each Player, cycle through Hands etc?
	# should a hand keep track of options for itself?
	# should options be persistent and then dynamically pulled for each hand?

# print player hand states
for player in game.players:
	count = 1
	print("{}'s Hand states are:\n".format(player.name))
	for hand in player.hands:
	  print("Hand {}: {}".format(count, hand.state))
	  count += 1

print("\n\n")

for player in game.players:
	print(player)

print("\n\n")

game.print_bet_tracker()

# Player enters name - how many players? **kwargs? (["Michael": 1, "Jason": 2"]) etc? Or **args? (["Michael, Jason"]) etc?
# Cards created
# Cards shuffled
# Cards dealt
# Continue to calculate hand for every Card dealt
# If either exceeds 21, other Player wins
# If either Player or Dealer hit 21, they win. Dealer wins if both are 21

##
