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
        return cls([])


class PlayCardPile(CardPile):
    __invisible_cards = {CardValue.FOUR}

    def __init__(self, cards: Cards):
        super().__init__(cards)
        self.__first_visible_currently = self.__first_visible(cards)

    @property
    def visible_top_card(self) -> None | Card:
        return self.__first_visible_currently

    def add_card(self, card: Card) -> None:
        super().add_card(card)
        self.__update_first_visible()
        return None

    def add_cards(self, cards: Cards) -> None:
        super().add_cards(cards)
        self.__update_first_visible()
        return None

    def clear(self) -> None:
        super().clear()
        self.__first_visible_currently = None
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

    def __update_first_visible(self) -> None:
        self.__first_visible_currently = self.__first_visible(self)
        return None

    @staticmethod
    def __first_visible(cards: Cards) -> Card | None:
        if len(cards) == 0:
            return None
        values = cards.values
        if len(values) == 1:
            if values[0] != CardValue.FOUR:
                return cards[0]
            return None
        for i in range(len(values) - 1, -1, -1):
            value = values[i]
            if value == CardValue.FOUR:
                continue
            if value == CardValue.JACK:
                if i != 0 and values[i-1] != CardValue.FOUR:
                    return cards[i]
                continue
            return cards[i]
        return None
