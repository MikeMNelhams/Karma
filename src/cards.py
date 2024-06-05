from __future__ import annotations

import random
from enum import Enum

from collections import Counter

from typing import Iterable, TypeVar


type CardValueCounts = dict[CardValue, int]


class Card:
    def __init__(self, suit: CardSuit, value: CardValue):
        self.__suit = suit
        self.__value = value

    def __hash__(self):
        return hash((self.value, self.suit.name))

    def __repr__(self) -> str:
        return f"{CARD_VALUE_NAMES[self.__value.value]}{self.__suit}"

    def __eq__(self, other: Card) -> bool:
        return self.suit == other.suit and self.value == other.value

    def __gt__(self, other: Card) -> bool:
        return self.value.value > other.value.value

    def __lt__(self, other: Card) -> bool:
        return self.value.value < other.value.value

    def __ge__(self, other: Card) -> bool:
        return self.value.value >= other.value.value

    def __le__(self, other: Card) -> bool:
        return self.value.value <= other.value.value

    @property
    def suit(self) -> CardSuit:
        return self.__suit

    @property
    def value(self) -> CardValue:
        return self.__value


CARD = TypeVar("CARD", bound=Card)


class Cards(list[Card]):
    def __init__(self, cards: Iterable[Card] | None = None):
        if cards is None:
            super().__init__([])
        elif isinstance(cards, Card):
            super().__init__([cards])
        else:
            super().__init__(cards)

    def __hash__(self):
        return hash(tuple(self))

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
        excluded_indices = set(indices)
        output = Cards((card for i, card in enumerate(self) if i in excluded_indices))
        self[:] = [card for i, card in enumerate(self) if i not in excluded_indices]
        return output

    def swap(self, index: int, card: Card) -> Card:
        card_before = self[index]
        self[index] = card
        return card_before

    def shuffle(self) -> None:
        random.shuffle(self)
        return None

    def contains(self, cards: Cards) -> bool:
        return len(self.search(cards)) == len(cards)

    def is_exclusively(self, card_value: CardValue) -> bool:
        return all(card.value == card_value for card in self)

    def search(self, cards: Cards) -> list[int]:
        # TODO Use binary search to speed it up a BIT
        target_cards = cards.copy()
        self_copy = self.copy()
        indices = []
        for i in range(len(target_cards) - 1, -1, -1):
            target_card = target_cards[i]
            for j in range(len(self_copy) - 1, -1, -1):
                card_checking = self_copy[j]
                if target_card == card_checking:
                    indices.append(j)
                    target_cards.pop(i)
        return indices

    def remove(self, cards: Cards) -> Cards:
        """ LIST difference (order preserved, duplicates preserved). self = x - y and returns (x - y)"""
        removed_cards = Cards()
        targets_counts = Counter(cards)
        leftovers = Cards()
        for i, x in enumerate(self):
            if x in targets_counts and targets_counts[x] > 0:
                targets_counts[x] -= 1
                removed_cards.add_card(x)
            else:
                leftovers.add_card(x)
        self[:] = leftovers
        return removed_cards

    def get(self, indices: list[int]) -> Cards:
        return Cards((self[i] for i in indices))

    def count_value(self, target_value: CardValue) -> int:
        return sum(1 if card.value == target_value else 0 for card in self)

    @property
    def values(self) -> list[CardValue]:
        if not self:
            return []
        return tuple(card.value for card in self)


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

    def __repr__(self) -> str:
        return f"{self.name}"

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: CardValue) -> bool:
        return self.value == other.value


CARD_VALUE_NAMES = ({x: str(x) for x in range(2, 10)} |
                    {10: "T", 11: "J", 12: "Q", 13: "K", 14: "A",
                     15: "J_K"})


SUITS = (CardSuit(CardColor.RED, "Hearts", "♥"),
         CardSuit(CardColor.RED, "Diamonds", "♦"),
         CardSuit(CardColor.BLACK, "Clubs", "♣"),
         CardSuit(CardColor.BLACK, "Spades", "♠"))


def non_six_value(counts: CardValueCounts) -> CardValue:
    keys = list(counts.keys())
    card_value1 = keys[0]
    card_value2 = keys[1]
    return card_value1 if card_value1 != CardValue.SIX else card_value2


def non_six_value_from_cards(cards: Cards) -> CardValue:
    for card in cards:
        if card.value != CardValue.SIX:
            return card.value
    raise TypeError(f"All cards are six or the cards are empty: {cards}")
