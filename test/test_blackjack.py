import unittest
# edit system path to start at root to look for modules
import sys
sys.path.append('..')

from app.blackjack import Player, Card, Game, Dealer, Hand

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

	# not working?
	def test_hand_returns_error_message_if_hand_less_than_zero(self):
		self.assertRaises(ValueError, self.hand.update_hand())

	def test_hand_count_is_num_type(self):
		self.assertIsInstance(self.hand.value, (int, float, complex))

	# does nothing - implement check to ensure correct error is thrown if below zero
	def test_hand_count_is_positive_or_zero(self):
		self.assertTrue(self.hand.value >= 0)

if __name__ == '__main__':
	unittest.main()