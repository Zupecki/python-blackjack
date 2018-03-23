import unittest
# edit system path to start at root to look for modules
import sys
sys.path.append('..')

from app.blackjack import Game, Player, Dealer, Hand, Card

class TestBlackjackPlayer(unittest.TestCase):

	def setUp(self):
		self.player = Player('Michael')

	def test_player_name_is_string(self):
		self.assertIsInstance(self.player.name, str)

	def test_player_hand_is_hand_object(self):
		self.assertIsInstance(self.player.hand, Hand)

class TestBlackjackHand(unittest.TestCase):

	def setUp(self):
		self.hand = Hand()

	def test_hand_value_is_num_type(self):
		self.assertIsInstance(self.hand.value, (int, float, complex))

	def test_hand_count_is_num_type(self):
		self.assertIsInstance(self.hand.value, (int, float, complex))

	def test_change_aces_brings_hand_to_below_21_when_bust_with_aces(self):
		# add 4 aces, hand value 44, cycle through and change three aces to value 1
		# for hand value of 14
		testCards = (Card("Diamonds", 11, "Ace"), Card("Clubs", 11, "Ace"),
		Card("Spades", 11, "Ace"), Card("Hearts", 11, "Ace"))

		for card in testCards:
			self.hand.insert_card(card)

		self.assertEqual(14, self.hand.value)

	def test_card_inserts_into_hand_correctly(self):
		card = Card("Diamonds", 10, "King")
		self.hand.insert_card(card)
		
		# check first index for card
		self.assertEqual(card, self.hand.cards['fixedCards'][0])

	def test_hand_value_is_correct(self):
		testCards = (Card("Diamond", 10, "Jack"), Card("Hearts", 2, "Two"))

		for card in testCards:
			self.hand.insert_card(card)

		self.assertEqual(12, self.hand.value)

if __name__ == '__main__':
	unittest.main()