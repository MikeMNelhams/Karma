import unittest

from src.cards import Cards, Card, CardValue, CardSuit, SUITS
from src.card_pile import PlayCardPile


class TestPlayCardPile_TopVisibleCard(unittest.TestCase):
    def test_empty_is_none(self):
        pile = self.__from_values([])
        self.assertIsNone(pile.visible_top_card)

    def test_fours_are_none(self):
        pile = self.__from_values([4, 4, 4])
        self.assertIsNone(pile.visible_top_card)

    def test_four_jack_is_none(self):
        pile = self.__from_values([4, 11])
        self.assertIsNone(pile.visible_top_card)

    def test_jack_is_jack(self):
        pile = self.__from_values([11])
        self.assertEqual(pile.visible_top_card.value, CardValue.JACK)

    def test_four_jack_repeating_is_none(self):
        pile = self.__from_values([4, 11, 4, 11, 4, 11])
        self.assertIsNone(pile.visible_top_card)

    def test_jack_four_is_jack(self):
        pile = self.__from_values([11, 4, 4, 4])
        self.assertEqual(pile.visible_top_card.value, CardValue.JACK)

    def test_all_valid_visible(self):
        values = [2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15]
        for value in values:
            pile = self.__from_values([value])
            self.assertEqual(pile.visible_top_card.value, CardValue(value))

            pile = self.__from_values([value, 4, 4, 4, 11, 4])
            self.assertEqual(pile.visible_top_card.value, CardValue(value))

    @staticmethod
    def __from_values(values: list[int], default_suit: CardSuit=SUITS[0]):
        return PlayCardPile(Cards([Card(default_suit, CardValue(value)) for value in values]))


class TestPlayCardPile_VisibleCards(unittest.TestCase):
    always_visibles = [2, 3, 5, 7, 8, 9, 10, 12, 13, 14, 15]
    sometimes_invisible = [6, 11]

    def test_init_empty(self):
        pile = self.__from_values([])
        self.assertEqual(pile.visibles, [])

    def test_init_four_is_invisible(self):
        pile = self.__from_values([4])
        self.assertEqual(pile.visibles, [0])

    def test_init_jack_is_visible(self):
        pile = self.__from_values([11])
        self.assertEqual(pile.visibles, [1])

    def test_init_six_is_visible(self):
        pile = self.__from_values([6])
        self.assertEqual(pile.visibles, [1])

    def test_init_fours_are_invisible(self):
        pile = self.__from_values([4, 4, 4])
        self.assertEqual(pile.visibles, [0, 0, 0])

    def test_init_four_jack_is_visible(self):
        pile = self.__from_values([4, 11])
        self.assertEqual(pile.visibles, [0, 0])

    def test_init_four_jack_repeating_all_invisible(self):
        pile = self.__from_values([4, 11, 4, 11, 4, 11])
        self.assertEqual(pile.visibles, [0, 0, 0, 0, 0, 0])

    def test_init_jack_four_is_visible(self):
        pile = self.__from_values([11, 4, 4, 4])
        self.assertEqual(pile.visibles, [1, 0, 0, 0])

    def test_init_all_valid_visibles(self):
        for value in self.always_visibles:
            pile = self.__from_values([value])
            self.assertEqual(pile.visibles, [1])

            pile = self.__from_values([4, value, 4, 4, 4, 11, 4])
            self.assertEqual(pile.visibles, [0, 1, 0, 0, 0, 0, 0])

    def test_add_card_unspecified(self):
        pile = self.__from_values([3])
        pile.add_card(Card(SUITS[0], CardValue(3)))
        pile.add_card(Card(SUITS[0], CardValue(4)))
        pile.add_card(Card(SUITS[0], CardValue(6)))
        pile.add_card(Card(SUITS[0], CardValue(11)))
        self.assertEqual(pile.visibles, [1, 1, 0, 1, 1])

    def test_add_card_specified(self):
        pile = self.__from_values([3])
        for i in range(2, 16):
            pile.add_card(Card(SUITS[0], CardValue(i)))
        self.assertEqual(pile.visibles, [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    def test_add_pop_empty_always_visible(self):
        pile = self.__from_values([])
        for value in self.always_visibles:
            pile.add_card(Card(SUITS[0], CardValue(value)))
            self.assertEqual(pile.visibles, [1])
            pile.pop_card()
            self.assertEqual(pile.visibles, [])

    def test_add_pop_empty_four(self):
        pile = self.__from_values([])
        pile.add_card(Card(SUITS[0], CardValue(4)))
        self.assertEqual(pile.visibles, [0])
        pile.pop_card()
        self.assertEqual(pile.visibles, [])

    def test_add_pop_empty_sometimes_invisible(self):
        pile = self.__from_values([])
        for value in self.sometimes_invisible:
            pile.add_card(Card(SUITS[0], CardValue(value)))
            self.assertEqual(pile.visibles, [1])
            pile.pop_card()
            self.assertEqual(pile.visibles, [])

    def test_clear(self):
        pile = self.__from_values([4, 11, 4, 3, 11])
        self.assertEqual(pile.visibles, [0, 0, 0, 1, 1])
        pile.clear()
        self.assertEqual(pile.visibles, [])

    def test_add_cards_empty_unspecified(self):
        pile = self.__from_values([])
        pile.add_cards(self.__cards_from_values([3, 4, 3, 4, 11, 2, 6]))
        self.assertEqual(pile.visibles, [1, 0, 1, 0, 1, 1, 1])

    def test_add_cards_specified(self):
        pile = self.__from_values([3])
        pile.add_cards(self.__cards_from_values([3, 4, 3, 4, 11, 2, 6]), are_visibles=[0, 1, 0, 0, 0, 1, 1])
        self.assertEqual(pile.visibles, [1, 0, 1, 0, 0, 0, 1, 1])

    def test_pop_multiple(self):
        pile = self.__from_values([4, 11, 3, 4, 6])
        self.assertEqual(pile.visibles, [0, 0, 1, 0, 1])
        pile.pop_multiple([0, 2])
        self.assertEqual(pile.visibles, [0, 0, 1])

    def test_remove_from_bottom(self):
        pile = self.__from_values([3, 4, 3, 4, 11, 7, 4, 4, 2, 6])
        self.assertEqual(pile.visibles, ([1, 0, 1, 0, 0, 1, 0, 0, 1, 1]))
        pile.remove_from_bottom(4)
        self.assertEqual(pile.visibles, ([0, 1, 0, 0, 1, 1]))

    def test_remove_from_bottom_empty(self):
        pile = self.__from_values([3, 4])
        self.assertEqual(pile.visibles, [1, 0])
        pile.remove_from_bottom(3)
        self.assertEqual(pile.visibles, [])

    @staticmethod
    def __cards_from_values(values: list[int], default_suit: CardSuit = SUITS[0]) -> Cards:
        return Cards([Card(default_suit, CardValue(value)) for value in values])

    def __from_values(self, values: list[int], default_suit: CardSuit = SUITS[0]) -> PlayCardPile:
        return PlayCardPile(self.__cards_from_values(values, default_suit=default_suit))


if __name__ == '__main__':
    unittest.main()
