from src.cards import Card, Cards, CardValue
from src.card_pile import CardPile
from src.hand import Hand
from src.karma import KarmaFaceUp, KarmaFaceDown


class Player:
    playable_options = {Hand: 0, KarmaFaceDown: 1, KarmaFaceUp: 2}

    def __init__(self, starting_hand: Hand, starting_face_down_karma: KarmaFaceDown, starting_face_up_karma: KarmaFaceUp):
        self.hand = starting_hand
        self.hand.sort()
        self.karma_face_down = starting_face_down_karma
        self.karma_face_up = starting_face_up_karma

    def __repr__(self) -> str:
        return f"Player(H{self.hand}, {self.__repr_karma()})"

    def __len__(self) -> int:
        return len(self.hand) + len(self.karma_face_up) + len(self.karma_face_down)

    def repr_debug(self) -> str:
        return f"Player({self.hand}, {self.__repr_karma_debug()})"

    def repr_invisible_hand(self) -> str:
        return f"Player({self.hand.repr_flipped()}, {self.__repr_karma()})"

    def __repr_karma(self) -> str:
        return f"FUK{self.karma_face_up}, FDK{self.karma_face_down.repr_flipped()}"

    def __repr_karma_debug(self) -> str:
        return f"FUK{self.karma_face_up}, FDK{self.karma_face_down}"

    @property
    def has_cards(self) -> bool:
        return len(self) != 0

    @property
    def playable_cards(self) -> Cards:
        if len(self.hand) > 0:
            return self.hand
        if len(self.karma_face_up) > 0:
            return self.karma_face_up
        if len(self.karma_face_down) > 0:
            return self.karma_face_down
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

    def swap_hand_card_with_karma(self, hand_index: int, karma_index: int) -> None:
        self.hand[hand_index], self.karma_face_up[karma_index] = self.karma_face_up[karma_index], self.hand[hand_index]
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
        if self.karma_face_up:
            total += self.karma_face_up.count_value(CardValue.JOKER)
        if self.karma_face_down:
            total += self.karma_face_down.count_value(CardValue.JOKER)
        return total
