from typing import Any, Callable, Iterable

from src.cards import Card
from src.card_pile import CardPile
from src.hand import Hand
from src.Poop import PoopFaceUp, PoopFaceDown


class Player:
    def __init__(self, starting_hand: Hand, starting_face_down_poop: PoopFaceDown, starting_face_up_poop: PoopFaceUp):
        self.hand = starting_hand
        self.poop_face_down = starting_face_down_poop
        self.poop_face_up = starting_face_up_poop

    def pickup(self, pile: CardPile) -> None:
        self.hand.add_cards(pile.cards)
        pile.clear()
        return None

    def pop_from_hand(self, index: int) -> Card:
        return self.hand.pop_card(index)

    def pop_from_hand_multiple(self, indices: Iterable[int]) -> None:
        return self.hand.pop_cards(indices)

    def swap_hand_card_with_poop(self, poop_index: int, hand_index: int) -> None:
        self.hand[hand_index], self.poop_face_up[poop_index] = self.poop_face_up[poop_index], self.poop_face_up[poop_index]
        return None

    def pop_from_face_up_poop(self, index: int) -> None:
        self.poop_face_up.pop_card(index)
        return None

    def pop_multiple_from_face_up_poop(self, indices: Iterable[int]) -> None:
        self.poop_face_up.pop_multiple(indices)
        return None

    def pop_from_face_down_poop(self, index: int) -> None:
        self.poop_face_down.pop_card(index)
        return None

    def pop_multiple_from_face_down_poop(self, indices: Iterable[int]) -> None:
        self.poop_face_down.pop_multiple(indices)
        return None

    def draw_card(self, pile: CardPile) -> None:
        self.hand.add_card(pile.pop_card(-1))

    def receive_card(self, card: Card) -> None:
        self.hand.add_card(card)
        return None

    def rotate_hand(self, hand: Hand) -> Hand:
        hand_before_rotation = self.hand
        self.hand = hand
        return hand_before_rotation
