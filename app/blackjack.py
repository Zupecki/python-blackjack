# Initial primary code for command line Blackjack - might split into separate files if necessary
# A Game has Players, a Dealer and a Deck of Cards
# A Player has Cards and set of actions
# A Deck has Cards or is Empty
import sys
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

# deal 2 cards to each player

for x in range(0,3):
  for player in game.players:
    game.dealer.deal_card(player, game.deck)
  game.dealer.deal_card(game.dealer, game.deck)

# show hand

game.show_players_hands()

# report how many cards are in the deck

print("\n{} cards in the deck.\n".format(game.deck.count))

# print players

game.print_players()

# print busted players - NOT WORKING!

for player in game.players:
  #if(player.bust == True):
    #print("{} is busted!".format(player.name))
  print("{} busted is {}".format(player.name, player.bust))

# Player enters name - how many players? **kwargs? (["Michael": 1, "Jason": 2"]) etc? Or **args? (["Michael, Jason"]) etc?
# Cards created
# Cards shuffled
# Cards dealt
# Continue to calculate hand for every Card dealt
# If either exceeds 21, other Player wins
# If either Player or Dealer hit 21, they win. Dealer wins if both are 21

##
