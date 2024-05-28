from typing import Iterable

from src.cards import Card, Cards


class Poop(Cards):
    def __init__(self, cards: Iterable[Card]):
        super().__init__(cards)

    def pop_card(self, index: int):
        self.pop(index)
        return None

    def pop_multiple(self, indices: int):
        return self.pop_multiple(indices)


class PoopFaceUp(Poop):
    def __init__(self, cards: Cards):
        super().__init__(cards)

    def swap(self, index: int, card: Card) -> Card:
        return self.swap(index, card)


class PoopFaceDown(Poop):
    def __init__(self, cards: Cards):
        super().__init__(cards)
