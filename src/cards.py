from __future__ import annotations

from typing import Iterable, TypeVar


class Card:
    def __init__(self, suit: CardSuit, value: CardValue):
        self.__suit = suit
        self.__value = value

    @property
    def suit(self) -> CardSuit:
        return self.__suit

    @property
    def value(self) -> CardValue:
        return self.__value


CARD = TypeVar("CARD", bound=Card)


class Cards(list[Card]):
    def __init__(self, cards: Iterable[Card]):
        super().__init__(cards)

    def pop_multiple(self, indices: Iterable[int]) -> Cards:
        self[:] = [card for i, card in enumerate(self) if i not in set(indices)]
        return Cards((card for i, card in enumerate(self) if i in set(indices)))

    def swap(self, index: int, card: Card) -> Card:
        card_before = self[index]
        self[index] = card
        return card_before


class CardSuit:
    def __init__(self, colour: CardColor, name: str):
        self.colour = colour
        self.name = name


class CardColor:
    RED = 0
    BLACK = 1


class CardValue:
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    JOKER = 15
