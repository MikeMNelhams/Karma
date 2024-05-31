from typing import Self

from cards import Card, Cards, CardValue


class CardPile(Cards):
    def __init__(self, cards: Cards):
        super().__init__(cards)

    def pop_card(self, index: int) -> Card:
        return self.pop(index)

    def remove_from_bottom(self, split_index: int) -> Cards:
        output = self[:split_index]
        self[:] = self[split_index:]
        return output

    @classmethod
    def empty(cls) -> Self:
        return CardPile([])


class PlayCardPile(CardPile):
    __invisible_cards = {CardValue.FOUR, CardValue.JACK}

    def __init__(self, cards: Cards):
        super().__init__(cards)
        self.__first_non_four = None

    @property
    def visible_top_card(self) -> None | Card:
        return self.__first_non_four

    def add_card(self, card: Card) -> None:
        super().add_card(card)
        if card.value != CardValue.FOUR:
            self.__first_non_four = card
        return None

    def add_cards(self, cards: Cards) -> None:
        super().add_cards(cards)
        card = cards[0]
        if self.visible_top_card is None and card.value in self.__invisible_cards:
            return None
        self.__first_non_four = card
        return None

    def clear(self) -> None:
        super().clear()
        self.__first_non_four = None
        return None

    @property
    def will_burn(self) -> bool:
        if len(self) < 4:
            return False
        total_run = 0
        major_value = self[-1]

        for card in reversed(self[:-1]):
            if card.value != major_value.value:
                total_run = 0
                major_value = card.value
            else:
                total_run += 1

            if total_run == 4:
                return True
        return False
