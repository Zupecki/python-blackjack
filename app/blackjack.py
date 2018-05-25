# Code for command line Blackjack; game loop
# by Michael Zupecki, 2018

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
						while hand.state['Active'] == True:
							# render turn
							game.render_turn(player, hand)

							# print options
							options = game.generate_options(hand)
							game.print_options(options, player, hand)

							# check hand
							if(hand.check_hand(player, game) == 'Break'):
								break

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

	# if at least one Player isn't bust
	if(game.allBust == False):
		# dealer hits
		game.dealer_hit()

		# dealer end state
		game.dealer.end_state(game)

	# test printing
	#test_output(game)

	# process game results and then print
	game.print_results(game.process_results())

	# play again?
	game.end()



