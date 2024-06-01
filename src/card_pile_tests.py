import unittest

from src.cards import Cards, Card, CardValue, CardSuit, SUITS
from src.card_pile import PlayCardPile


class PlayCardPile_TopVisibleCard(unittest.TestCase):
    def test_empty_is_none(self):
        pile = self.__from_values([])
        self.assertIsNone(pile.visible_top_card)

    def fours_are_none(self):
        pile = self.__from_values([4, 4, 4])
        self.assertIsNone(pile.visible_top_card)

    def four_jack_is_none(self):
        pile = self.__from_values([4, 11])
        self.assertIsNone(pile.visible_top_card)

    def jack_is_jack(self):
        pile = self.__from_values([11])
        self.assertEqual(pile.visible_top_card, CardValue.JACK)

    def four_jack_repeating_is_none(self):
        pile = self.__from_values([4, 11, 4, 11, 4, 11])
        self.assertIsNone(pile.visible_top_card)

    def jack_four_is_jack(self):
        pile = self.__from_values([11, 4, 4, 4])
        self.assertEqual(pile.visible_top_card, CardValue.JACK)

    def all_valid_visible(self):
        values = [2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15]
        for value in values:
            pile = self.__from_values([value])
            self.assertEqual(pile.visible_top_card, CardValue(value))

            pile = self.__from_values([value, 4, 4, 4, 11, 4])
            self.assertEqual(pile.visible_top_card, CardValue(value))

    @staticmethod
    def __from_values(values: list[int], default_suit: CardSuit=SUITS[0]):
        return PlayCardPile(Cards([Card(default_suit, value) for value in values]))


if __name__ == '__main__':
    unittest.main()
