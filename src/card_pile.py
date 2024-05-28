from cards import Card, Cards


class CardPile:
    def __init__(self, cards: Cards):
        self.cards = [card for card in cards]

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
