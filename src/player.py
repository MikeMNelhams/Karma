from src.cards import Card, Cards
from src.card_pile import CardPile
from src.hand import Hand
from src.poop import PoopFaceUp, PoopFaceDown


class Player:
    def __init__(self, starting_hand: Hand, starting_face_down_poop: PoopFaceDown, starting_face_up_poop: PoopFaceUp):
        self.hand = starting_hand
        self.poop_face_down = starting_face_down_poop
        self.poop_face_up = starting_face_up_poop

    def __repr__(self) -> str:
        return f"Player(H{self.hand}, {self.__repr_poop()})"

    def repr_invisible_hand(self) -> str:
        return f"Player({self.hand.repr_flipped()}, {self.__repr_poop()})"

    def __repr_poop(self) -> str:
        return f"FUP{self.poop_face_up}, FDP{self.poop_face_down.repr_flipped()}"

    @property
    def has_cards(self) -> bool:
        return len(self.hand) + len(self.poop_face_up) + len(self.poop_face_down) != 0

    @property
    def playable_cards(self) -> Cards:
        if len(self.hand) > 0:
            return self.hand
        if len(self.poop_face_up) > 0:
            return self.poop_face_up
        if len(self.poop_face_down) > 0:
            return self.poop_face_down
        return Cards()

    def pickup(self, pile: CardPile) -> None:
        self.hand.add_cards(pile)
        pile.clear()
        return None

    def pop_from_playable(self, indices: list[int]) -> Cards:
        removed = self.playable_cards.pop_multiple(indices)
        return removed

    def swap_hand_card_with_poop(self, hand_index: int, poop_index: int) -> None:
        self.hand[hand_index], self.poop_face_up[poop_index] = self.poop_face_up[poop_index], self.hand[hand_index]
        return None

    def draw_card(self, pile: CardPile) -> None:
        self.hand.add_card(pile.pop_card(-1))
        return None

    def receive_card(self, card: Card) -> None:
        self.hand.add_card(card)
        return None

    def rotate_hand(self, hand: Hand) -> Hand:
        hand_before_rotation = self.hand
        self.hand = hand
        return hand_before_rotation

    def shuffle_hand(self) -> None:
        self.hand.shuffle()
        return None
