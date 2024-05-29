from typing import Iterable

from enum import Enum

from collections import deque

from src.cards import Cards, Card, CardValue
from src.hand import Hand
from src.player import Player
from src.card_pile import CardPile, PlayCardPile


class BoardPlayOrder(Enum):
    UP = 0
    DOWN = 1


class Board:
    INVALID_ACTIONS = {"draw_card", "receive_card", "rotate_hand"}


    def __init__(self, players: Iterable[Player], draw_pile: CardPile, who_starts: int):
        self.players = deque(players)
        self.draw_pile = draw_pile

        self.burn_pile = CardPile([])
        self.play_pile = PlayCardPile([])

        self.play_order = BoardPlayOrder.UP
        self.cards_are_flipped = False
        self.effect_multiplier = 1
        self.player_index = who_starts

    def play_turn(self) -> None:
        current_player = self.players[self.player_index]

        self.executePlayerAction(current_player)

        self.player_index += 1
        self.player_index %= len(self.players)

    def executePlayerAction(self, player: Player):
        # TRIPLE DISPATCH
        # 1. Choosing player method based on user input
        # - Doing a dictionary lookup based on user input
        # 2. Choosing the input selecting method which asks the user for inputs about the action they want to execute
        # - Doing a dictionary lookup based on action_name
        # 3. Execute the method which asks for user input
        # 4. Execute the player action with given input

        # not_played_legal_move = True
        # while not_played_legal_move:
        #     action_name = ""
        #     while not hasattr(player, action_name) or action_name in Board.INVALID_ACTIONS:
        #         if action_name == "exit":
        #             raise InterruptedError("Quiting game!")
        #         action_name = input("What would you like to do? ").lower()
        #
        #     if action_name == "pickup":
        #         player.pickup(self.play_pile)
        #         return None
        #     if action_name == "pop_from_hand":
        #         index = input("What card INDEX would you like to play?")
        #
        #         if not player.hand.is_valid_card_index(index):
        #             continue
        #
        #         if not self.is_legal_play(player.hand[index]):
        #             print(f"That card cannot be played on top of {self.play_pile}")
        #             continue

        return None

    def play_card(self, card: Card) -> None:
        self.play_pile.add_card_to_top(card)

        match card.value:
            case CardValue.TWO:
                self.__play_two()
            case CardValue.THREE:
                self.__play_three()
            case CardValue.FOUR:
                self.__play_four()
            case CardValue.FIVE:
                self.__play_five()
            case CardValue.SIX:
                self.__play_six()
            case CardValue.SEVEN:
                self.__play_seven()
            case CardValue.EIGHT:
                self.__play_eight()
            case CardValue.NINE:
                self.__play_nine()
            case CardValue.TEN:
                self.__play_ten()
            case CardValue.JACK:
                self.__play_jack()
            case CardValue.QUEEN:
                self.__play_queen()
            case CardValue.KING:
                self.__play_king()
            case CardValue.ACE:
                self.__play_ace()
            case CardValue.JOKER:
                self.__play_joker()

        if card.value not in (CardValue.THREE, CardValue.JACK):
            self.effect_multiplier = 1
        return None

    def __play_two(self) -> None:
        self.play_order = BoardPlayOrder.UP
        return None

    def __play_three(self) -> None:
        self.effect_multiplier *= 2
        return None

    def __play_four(self) -> None:
        return None

    def __play_five(self) -> None:
        hands = deque([player.hand for player in self.players])
        hands.rotate(self.effect_multiplier)
        for i in range(len(self.players)):
            self.players[i].hand = hands[i]
        return None

    def __play_six(self) -> None:
        return None

    def __play_seven(self) -> None:
        if self.effect_multiplier != 1:
            return None

        self.play_order = 1 - self.play_order
        return None

    def __play_eight(self) -> None:
        if self.effect_multiplier != 1:
            return None
        for i in range(1, min(self.player_index + 1, len(self.players) - self.player_index) + 1):
            self.players[self.player_index + i], self.players[self.player_index - i] = self.players[self.player_index - i], self.players[self.player_index + i]
        return None

    def __play_nine(self) -> None:
        self.player_index += self.effect_multiplier
        return None

    def __play_ten(self) -> None:
        self.effect_multiplier = 1
        self.play_order = 1 - self.play_order
        self.burn(is_joker=False)
        return None

    def __play_jack(self) -> None:
        if len(self.play_pile) <= 1:
            return None
        self.play_card(self.play_pile.cards[-2])
        return None

    def __play_queen(self) -> None:
        # TODO
        pass

    def __play_king(self) -> None:
        # TODO
        pass

    def __play_ace(self) -> None:
        for _ in range(self.effect_multiplier):
            self.cards_are_flipped = not self.cards_are_flipped
        return None

    def __play_joker(self) -> None:
        self.burn_pile.add_card_to_top(self.play_pile.cards[-1])
        self.burn(is_joker=True)

        index = -1
        while not (0 <= index <= len(self.players)):
            index = input("Who would you like to be JOKERED? ")

        self.players[index].pickup(self.play_pile)
        return None

    def burn(self, is_joker: bool) -> None:
        if is_joker:
            self.burn_pile.add_card_to_top(self.burn_pile.cards.pop())
            return None
        self.burn_pile.add_cards_to_top(self.play_pile.cards)
        self.play_pile.clear()
        self.player_index -= 1
        return None

    def is_legal_play(self, play_card: Card) -> bool:
        if self.cards_are_flipped:
            return True

        if not self.play_pile and play_card.value != CardValue.JOKER:
            return True

        if play_card.value == CardValue.JOKER:
            return self.play_pile.pop_card(-1).value == CardValue.ACE

        first_non_four = self.play_pile.first_non_four
        if first_non_four is None:
            return True

        if self.play_order == BoardPlayOrder.UP:
            return play_card.value >= first_non_four.value
        return play_card.value <= first_non_four.value
