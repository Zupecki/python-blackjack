# Initial primary code for command line Blackjack - might split into separate files if necessary
# A Game has Players, a Dealer and a Deck of Cards
# A Player has Cards and set of actions
# A Deck has Cards or is Empty
import sys
import random
import os
sys.path.append('..')

import src.classes as blackjack

def test_output(game):
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


# GAME LOGIC

# Build game object, then set it up with Players, Dealer and Deck
game = blackjack.Game()
game.setup()

while game.play != False:
	# check at least one Player has enough cash
	if(not game.check_players_money()):
		break

	# Betting round
	game.collect_bets()

	# deal 2 cards to each player, including dealer
	game.initial_deal()

	# CORE LOOP
	while game.playerRound != False:
		for player in game.players:
			if(player.state['Active'] == True):
				turn = True
				# print Player details here - name, cash, hand info?
				while(turn == True):
					for hand in player.hands:

						# render initial turn if Blackjack, allow player to keep hitting hand while hand is Active
						if(hand.value == 21):
							game.turn_render(player, hand)
						
						while hand.state['Active'] == True:
							# render turn
							game.turn_render(player, hand)

							# print options
							options = game.generate_options(hand)
							game.print_options(options, player, hand)

							# get selection, then retrieve option method
							choice = blackjack.num_range_input_validation(int, 1, len(options), "What would you like to do with Hand {}?".format(hand.num), "selection must be between option range")
							option = game.menu_select(choice, options) # return correct option method

							# call option and pass in player and hand objects
							option(player, hand)

						# check if Player still has any active Hand (maybe new Hand was created via split)
						turn = False
						for hand in player.hands:
							if(hand.state['Active'] == True):
								turn = True

					# after Player has acted on all Hands, check if still in the game
					player.end_state(game)

		# bail out of game
		game.playerRound = False

	# check if at least one Player isn't Bust
	game.check_all_bust()

	# wipe console
	zeroHold = os.system("clear")

	# if at least one Player isn't bust
	if(game.allBust == False):
		# dealer hits
		game.dealer_hit()

		# dealer end state
		game.dealer.end_state(game)

		# wipe console
		zeroHold = os.system("clear")

		# show dealers hand
		print("ROUND RESULTS:\n")
		print("Dealer's final hand -")
		print("Value: {}".format(game.dealer.hands[0].value))
		game.dealer.show_hand(game.dealer.hands[0])

		# clean up code
		# FORMATTING; 
			# Have Round number, and Title, always be at the top (move out of render_turn),
			# Have dealer cards print one at a time,
			# Weird extra newline after first turn in formatting
			# Have each Player's result print one at a time
			# Bug; if Player hits instant Blackjack, print wipe not working

	# test printing
	#test_output(game)

	# process game results and then print
	game.print_results(game.process_results())

	# play again?
	game.end()



