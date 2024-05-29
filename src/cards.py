from __future__ import annotations

import random
from enum import Enum

from typing import Iterable, TypeVar


class Card:
    def __init__(self, suit: CardSuit, value: CardValue):
        self.__suit = suit
        self.__value = value

    def __repr__(self) -> str:
        return f"{CARD_VALUE_NAMES[self.__value.value]}{self.__suit}"

    @property
    def suit(self) -> CardSuit:
        return self.__suit

    @property
    def value(self) -> CardValue:
        return self.__value


CARD = TypeVar("CARD", bound=Card)


class Cards(list[Card]):
    def __init__(self, cards: Iterable[Card] = None):
        if cards is None:
            super().__init__([])
        else:
            super().__init__(cards)

    def repr_flipped(self):
        unknowns = ["??" for _ in self]
        middle_str = ", ".join(unknowns)
        return f"[{middle_str}]"

    def add_card(self, card: Card) -> None:
        self.append(card)
        return None

    def add_cards(self, cards: Cards) -> None:
        for card in cards:
            self.add_card(card)
        return None

    def pop_multiple(self, indices: Iterable[int]) -> Cards:
        self[:] = [card for i, card in enumerate(self) if i not in set(indices)]
        return Cards((card for i, card in enumerate(self) if i in set(indices)))

    def swap(self, index: int, card: Card) -> Card:
        card_before = self[index]
        self[index] = card
        return card_before

    def shuffle(self) -> None:
        random.shuffle(self)
        return None


class CardSuit:
    def __init__(self, colour: CardColor, name: str, shorthand: str):
        self.colour = colour
        self.name = name
        self.shorthand = shorthand

    def __repr__(self) -> str:
        return self.shorthand


class CardColor:
    RED = 0
    BLACK = 1


class CardValue(Enum):
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


CARD_VALUE_NAMES = ({x: str(x) for x in range(2, 10)} |
                    {10: "T", 11: "J", 12: "Q", 13: "K", 14: "A",
                     15: "J_K"})


SUITS = (CardSuit(CardColor.RED, "Hearts", "♥"),
         CardSuit(CardColor.RED, "Diamonds", "♦"),
         CardSuit(CardColor.BLACK, "Clubs", "♣"),
         CardSuit(CardColor.BLACK, "Spades", "♠"))
