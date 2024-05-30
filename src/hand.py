from typing import Iterable

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
