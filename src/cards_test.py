import unittest

from src.cards import Cards, Card, CardSuit, CardValue, SUITS


class TestCards_Creation(unittest.TestCase):
    def test_empty_cards(self):
        cards = Cards()
        self.assertFalse(cards)
        self.assertEqual(len(cards), 0)

    def test_empty_cards_list_input(self):
        cards = Cards([])
        self.assertFalse(cards)
        self.assertEqual(len(cards), 0)

    def test_cards_single_card(self):
        c2 = Card(SUITS[0], CardValue(2))
        cards = Cards(c2)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0], c2)

    def test_cards_multiple_cards_list(self):
        c2 = Card(SUITS[0], CardValue(2))
        c6 = Card(SUITS[1], CardValue(6))
        cards = Cards([c2, c6])
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0], c2)
        self.assertEqual(cards[1], c6)

    def test_contains_positive(self):
        c2 = Card(SUITS[0], CardValue(2))
        c6 = Card(SUITS[1], CardValue(6))
        cards = Cards([c2, c6])
        self.assertTrue(cards.contains(Cards([c2])))
        self.assertTrue(cards.contains(Cards([c6])))


if __name__ == '__main__':
    unittest.main()
