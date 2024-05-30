from src.cards import Card, Cards, CardValue
from src.card_pile import CardPile
from src.hand import Hand
from src.poop import PoopFaceUp, PoopFaceDown


class Player:
    playable_options = {Hand: 0, PoopFaceDown: 1, PoopFaceUp: 2}

    def __init__(self, starting_hand: Hand, starting_face_down_poop: PoopFaceDown, starting_face_up_poop: PoopFaceUp):
        self.hand = starting_hand
        self.hand.sort()
        self.poop_face_down = starting_face_down_poop
        self.poop_face_up = starting_face_up_poop

    def __repr__(self) -> str:
        return f"Player(H{self.hand}, {self.__repr_poop()})"

    def __len__(self) -> int:
        return len(self.hand) + len(self.poop_face_up) + len(self.poop_face_down)

    def repr_debug(self) -> str:
        return f"Player({self.hand}, {self.__repr_poop_debug()})"

    def repr_invisible_hand(self) -> str:
        return f"Player({self.hand.repr_flipped()}, {self.__repr_poop()})"

    def __repr_poop(self) -> str:
        return f"FUP{self.poop_face_up}, FDP{self.poop_face_down.repr_flipped()}"

    def __repr_poop_debug(self) -> str:
        return f"FUP{self.poop_face_up}, FDP{self.poop_face_down}"

    @property
    def has_cards(self) -> bool:
        return len(self) != 0

    @property
    def playable_cards(self) -> Cards:
        if len(self.hand) > 0:
            return self.hand
        if len(self.poop_face_up) > 0:
            return self.poop_face_up
        if len(self.poop_face_down) > 0:
            return self.poop_face_down
        return Cards()

    @property
    def playing_from(self) -> int:
        return self.playable_options[self.playable_cards.__class__]

    def pickup(self, pile: CardPile) -> None:
        self.hand.add_cards(pile)
        pile.clear()
        return None

    def pop_from_playable(self, indices: list[int]) -> Cards:
        removed = self.playable_cards.pop_multiple(indices)
        return removed

    def swap_hand_card_with_poop(self, hand_index: int, poop_index: int) -> None:
        self.hand[hand_index], self.poop_face_up[poop_index] = self.poop_face_up[poop_index], self.hand[hand_index]
        self.hand.sort()
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

    @property
    def number_of_jokers(self) -> None:
        return self.__count_jokers()

    def __count_jokers(self) -> int:
        total = 0
        if self.hand:
            total += self.hand.count_value(CardValue.JOKER)
        if self.poop_face_up:
            total += self.poop_face_up.count_value(CardValue.JOKER)
        if self.poop_face_down:
            total += self.poop_face_down.count_value(CardValue.JOKER)
        return total
