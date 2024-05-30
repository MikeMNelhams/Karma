from typing import Iterable

from bisect import insort
from heapq import merge as heapq_merge

from src.cards import Card, Cards


class Hand(Cards):
    def __init__(self, cards: Iterable[Card]):
        super().__init__(cards)

    def pop_card(self, index: int) -> Card:
        return self.pop(index)

    def pop_cards(self, indices: list[int]) -> Cards:
        return self.pop_multiple(indices)

    def is_valid_card_index(self, index: int) -> bool:
        return not (0 <= index <= len(self))

    def shuffle(self) -> None:
        super().shuffle()
        return None

    def add_card(self, card: Card) -> None:
        insort(self, card)
        return None

    def add_cards(self, cards: Cards) -> None:
        self[:] = list(heapq_merge(self, sorted(cards)))
        return None
