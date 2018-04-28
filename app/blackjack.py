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
			turn = True
			# print Player details here - name, cash, hand info?
			while(turn == True):
				for hand in player.hands:
					# allow player to keep hitting hand while hand is Active
					while hand.state['Active'] == True:
						print("\n-- ROUND 1 --\nDealers Hand:\n")
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

					# check if Player still has any active Hand (maybe new Hand was created via split)
					turn = False
					for hand in player.hands:
						if(hand.state['Active'] == True):
							turn = True

			# after Player has acted on all Hands, check if still in the game
			player.end_state()
		else:
			print("Sorry Player {} ({}), you only have ${} and the minimum bet is $100")

	# bail out of game
	game.play = False

# dealer hits
game.dealer_hit()

# dealer end state
game.dealer.end_state()

# show dealers hand
print("\n-------\nDealers Hand: ")
game.dealer.show_hand(game.dealer.hands[0])
print("Dealers Hand worth: {}".format(game.dealer.hands[0].value))

	# flush bet tracker
	# FORMATTING - MAKE PRETTY

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

game.process_results()

# play again? (needs to moved back up, or could create brand new game and import Players)
print("Would you like to play another round, Y/N?")

while True:
	choice = input().upper()

	if(choice == 'Y' or choice == 'N'):
		if(choice == 'Y'):
			# reset bet tracker and game, loop again
		elif(choice == 'N'):
			break
	else:
		print("Sorry, must be Y or N, try again.")
		continue

# Player enters name - how many players? **kwargs? (["Michael": 1, "Jason": 2"]) etc? Or **args? (["Michael, Jason"]) etc?
# Cards created
# Cards shuffled
# Cards dealt
# Continue to calculate hand for every Card dealt
# If either exceeds 21, other Player wins
# If either Player or Dealer hit 21, they win. Dealer wins if both are 21

##
