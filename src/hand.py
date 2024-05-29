from typing import Iterable

import random

from src.cards import Card, Cards


class Hand(Cards):
    def __init__(self, cards: Iterable[Card]):
        super().__init__(cards)

    def add_card(self, card: Card) -> None:
        self.append(card)
        return None

    def add_cards(self, cards: Cards) -> None:
        for card in cards:
            self.add_card(card)
        return None

    def pop_card(self, index: int) -> Card:
        return self.pop(index)

    def pop_cards(self, indices: list[int]) -> list[Card]:
        return self.pop_multiple(indices)

    def shuffle(self) -> None:
        random.shuffle(self)
        return None

    def is_valid_card_index(self, index: int) -> bool:
        return not (0 <= index <= len(self))
