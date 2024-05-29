from cards import Card, Cards, CardValue


class CardPile(Cards):
    def __init__(self, cards: Cards):
        super().__init__(cards)

    def pop_card(self, index: int) -> Card:
        return self.pop(index)


class PlayCardPile(CardPile):
    def __init__(self, cards: Cards):
        super().__init__(cards)
        self.first_non_four = None

    def add_card(self, card: Card) -> None:
        super().add_card(card)
        if card.value != CardValue.FOUR:
            self.first_non_four = card
        return None

    def add_cards(self, cards: Cards) -> None:
        super().add_cards(cards)
        for card in reversed(cards):
            if card.value != CardValue.FOUR:
                self.first_non_four = card
                return None
        return None

    def clear(self) -> None:
        super().clear()
        self.first_non_four = None
        return None
