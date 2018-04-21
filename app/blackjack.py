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

# Game loop - CLEAN UP!
while game.play != False:
	for player in game.players:
		if(player.state['Active'] == True):
			# print Player details here - name, cash, hand info?
			for hand in player.hands:
				# allow player to keep hitting hand while hand is Active
				while hand.state['Active'] == True:
					print("Dealers Hand:\n")
					game.dealer.show_hand(game.dealer.hands[0])

					print("\nPlayer {} ({}) - what would you like to do with Hand {}?\n".format(player.num, player.name, hand.num))
					player.show_hand(hand)
					game.generate_options(hand)
					game.print_options()

					choice = input()
					option = game.menu_select(choice) # return correct option method

					# // redundant code, leaving for record
					#optionArgs = blackjack.get_arg_names(option)

					# call option and pass in player and hand objects
					option(player, hand)

					# SPLIT NOT WORKING AS SECOND HAND NEVER PROPOSITIONED FOR PLAY. MAYBE
					# NOT ADDED TO FOR LOOP SINCE CODE ALREADY RUNNING?

			# after Player has acted on all Hands, check if still in the game
			player.check_active()
		else:
			print("Sorry Player {} ({}), you only have ${} and the minimum bet is $100")

	# bail out of game
	game.play = False

# show dealers hand
game.dealer.hands[0].cards['allCards'][1].flip_card()
print("\n-------\nDealers Hand: ")
game.dealer.show_hand(game.dealer.hands[0])
print("Dealers Hand worth: {}".format(game.dealer.hands[0].value))

	# dealer behaviour - keep hitting until between 17 and 21
	# check if anyone has hit Blackjack and announce winners
	# pay out results, flush bet tracker

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
