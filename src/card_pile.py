from typing import Self, Iterable

from cards import Card, Cards, CardValue


class CardPile(Cards):
    def __init__(self, cards: Cards):
        super().__init__(cards)

    def pop_card(self, index: int=-1) -> Card:
        return self.pop(index)

    def remove_from_bottom(self, split_index: int) -> Cards:
        output = self[:split_index]
        self[:] = self[split_index:]
        return output

    @classmethod
    def empty(cls) -> Self:
        return cls([])


class PlayCardPile(CardPile):
    __invisible_cards = {CardValue.FOUR}

    def __init__(self, cards: Cards):
        super().__init__(cards)
        self.__visibles = self.__are_visibles(cards)

    @property
    def visibles(self) -> list[int]:
        return self.__visibles

    @property
    def visible_top_card(self) -> None | Card:
        if len(self.__visibles) == 0:
            return None
        if len(self.__visibles) == 1:
            if self.__visibles[0]:
                return self[0]
            else:
                return None
        for i in range(len(self)-1, -1, -1):
            visible = self.__visibles[i]
            if visible:
                return self[i]
        return None

    def add_card(self, card: Card, is_visible: bool | None=None) -> None:
        super().add_card(card)
        if is_visible is None:
            visibility = 1
            if card.value == CardValue.FOUR:
                visibility = 0
            self.__visibles.append(visibility)
        elif is_visible:
            self.__visibles.append(1)
        elif not is_visible:
            self.__visibles.append(0)
        return None

    def add_cards(self, cards: Cards, are_visibles: list[bool] | None=None) -> None:
        visibilities = are_visibles
        if are_visibles is None:
            visibilities = [1 if card.value != CardValue.FOUR else 0 for card in cards]
        assert len(visibilities) == len(cards), ValueError(f"{are_visibles}, {cards}")
        for card, visibility in zip(cards, visibilities):
            self.add_card(card, visibility)
        return None

    def pop_card(self, index: int=-1) -> Card:
        self.__visibles.pop(index)
        return super().pop_card(index)

    def pop_multiple(self, indices: Iterable[int]) -> Cards:
        excluded_indices = set(indices)
        self.__visibles = [x for i, x in enumerate(self.__visibles) if i not in excluded_indices]
        return super().pop_multiple(indices)

    def clear(self) -> None:
        super().clear()
        self.__visibles = []
        return None

    def remove_from_bottom(self, split_index: int) -> Cards:
        self.__visibles = self.__visibles[split_index:]
        return super().remove_from_bottom(split_index)

    def shuffle(self) -> None:
        raise NotImplementedError("Not supported yet for PlayCardPile")

    def remove(self, cards: Cards) -> Cards:
        raise NotImplementedError("Not supported yet for PlayCardPile")

    def contains_min_length_run(self, run_length: int = 4):
        k = run_length
        if len(self) < k:
            return False
        total_run = 1
        major_value = self[-1]

        for card in reversed(self[:-1]):
            if card.value == major_value.value:
                total_run += 1
            else:
                total_run = 1
                major_value = card.value

            if total_run == k:
                return True
        return False

    @staticmethod
    def __are_visibles(cards: Cards) -> list[int]:
        if len(cards) == 0:
            return []
        if len(cards) == 1:
            return [int(cards[0].value != CardValue.FOUR)]

        visibles = [True for _ in range(len(cards))]
        values = cards.values
        for i in range(len(values) - 1, -1, -1):
            value = values[i]
            if value == CardValue.FOUR:
                visibles[i] = False
            if value == CardValue.JACK and i != 0 and values[i-1] == CardValue.FOUR:
                visibles[i] = False
        return visibles
