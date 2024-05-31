from typing import Iterable

from src.cards import Card, Cards


class Karma(Cards):
    def __init__(self, cards: Iterable[Card]):
        super().__init__(cards)

    def pop_card(self, index: int):
        self.pop(index)
        return None

    def pop_multiple(self, indices: int):
        return self.pop_multiple(indices)


class KarmaFaceUp(Karma):
    def __init__(self, cards: Cards):
        super().__init__(cards)

    def swap(self, index: int, card: Card) -> Card:
        return self.swap(index, card)


class KarmaFaceDown(Karma):
    def __init__(self, cards: Cards):
        super().__init__(cards)
