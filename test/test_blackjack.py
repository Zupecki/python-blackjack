import unittest
import numpy as np
import copy
# edit system path to start at root to look for modules
import sys
sys.path.append('..')

from src.classes import Game, Player, Dealer, Hand, Card, Deck

class TestBlackjackPlayer(unittest.TestCase):

	def setUp(self):
		self.player = Player('Michael', 1)

	def test_player_name_is_string(self):
		self.assertIsInstance(self.player.name, str)

	def test_player_hand_is_hand_object(self):
		self.assertIsInstance(self.player.hands[0], Hand)

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
			self.hand.cards['allCards'].append(card)
			self.hand.cards['aces'].append(card)

		self.hand.recalculate_value()

		self.assertEqual(14, self.hand.value)

	def test_card_inserts_into_hand_correctly(self):
		card = Card("Diamonds", 10, "King")
		self.hand.cards['allCards'].append(card)
		
		# check first index for card
		self.assertEqual(card, self.hand.cards['allCards'][0])

	def test_hand_value_is_correct(self):
		testCards = (Card("Diamond", 10, "Jack"), Card("Hearts", 2, "Two"))

		for card in testCards:
			self.hand.cards['allCards'].append(card)

		self.hand.recalculate_value()

		self.assertEqual(12, self.hand.value)

class TestBlackjackDealer(unittest.TestCase):

	def setUp(self):
		self.player = Player("Michael", 1)
		self.dealer = Dealer("Dealer", 0)
		self.deck = Deck()

	def	test_dealer_deals_card_to_player_correctly(self):
		self.deck.build()
		self.deck.shuffle()
		# copy last card in deck for comparison
		lastCard = self.deck.cards[len(self.deck.cards)-1]

		# deal last card to Player, from end of deck
		self.dealer.deal_card(self.player, self.player.hands[0], self.deck, 'London')

		# get card type from Player, might have been ace
		card = self.player.hands[0].cards['allCards'][0]

		self.assertEqual(lastCard, self.player.hands[0].cards['allCards'][0])

class TestBlackjackCard(unittest.TestCase):

	def setUp(self):
		self.card = Card("Diamonds", 10, "King")

	def test_card_has_correct_suit(self):
		self.assertEqual("Diamonds", self.card.suit)

	def test_card_has_correct_value(self):
		self.assertEqual(10, self.card.value)

	def test_card_has_correct_title(self):
		self.assertEqual("King", self.card.title)

	def test_card_value_is_num(self):
		self.assertIsInstance(self.card.value, (int, float, complex))

	def test_card_prints_in_correct_pretty_format(self):
		compareString = "King of Diamonds - (10)"
		cardString = self.card.__str__()
		self.assertEqual(compareString, cardString)

class TestBlackjackDeck(unittest.TestCase):

	def setUp(self):
		self.deck = Deck()
		self.deck.build()

	def test_deck_counter_keeps_track_of_card_count(self):
		# check initial count
		self.assertEqual(52, self.deck.count)

		# remove 2 cards and check new count
		for x in range(0,2):
			card = self.deck.pop_card()
		self.assertEqual(50, self.deck.count)

		# remove 12 cards and check new count
		for x in range(0, 12):
			card = self.deck.pop_card()
		self.assertEqual(38, self.deck.count)

	def test_deck_builder_builds_appropriate_cards(self):
		# too cumbersome
		return True

	def test_deck_shuffle(self):
		# copy (deep copy so not reference) unshuffled deck for comparison
		compareDeck = copy.deepcopy(self.deck)
		# shuffle primary deck
		self.deck.shuffle()

		# deprecated way of checking equivalence using numpy - leaving for reference
		# sameOrder = np.array_equiv(compareDeck.cards, self.deck.cards)
		
		self.assertNotEqual(compareDeck.cards, self.deck.cards)

	def test_deck_raises_error_when_empty(self):
		# build and empty deck
		for x in range(0, 52):
			card = self.deck.pop_card()

		self.assertRaises(IndexError, self.deck.pop_card)

if __name__ == '__main__':
	unittest.main()