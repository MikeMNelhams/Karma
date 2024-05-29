from cards import Card, Cards, CardValue


class CardPile:
    def __init__(self, cards: Cards):
        self.cards = [card for card in cards]

    def __bool__(self) -> bool:
        return len(self) != 0

    def __len__(self) -> int:
        return len(self.cards)

    def add_card_to_top(self, card: Card) -> None:
        self.cards.append(card)
        return None

    def add_cards_to_top(self, cards: Cards) -> None:
        for card in cards:
            self.add_card_to_top(card)
        return None

    def pop_card(self, index: int) -> Card:
        return self.cards.pop(index)

    def clear(self) -> None:
        self.cards = []
        return None


class PlayCardPile(CardPile):
    def __init__(self, cards: Cards):
        super().__init__(cards)
        self.first_non_four = None

    def add_card_to_top(self, card: Card) -> None:
        super().add_card_to_top(card)
        if card.value != CardValue.FOUR:
            self.first_non_four = card
        return None

    def add_cards_to_top(self, cards: Cards) -> None:
        super().add_cards_to_top(cards)
        for card in reversed(cards):
            if card.value != CardValue.FOUR:
                self.first_non_four = card
                return None
        return None

    def clear(self) -> None:
        super().clear()
        self.first_non_four = None
        return None
