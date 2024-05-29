from __future__ import annotations

from typing import Any, Callable, Iterable

from abc import ABC, abstractmethod
from enum import Enum

from collections import deque

from src.cards import Cards, Card, CardValue
from src.hand import Hand
from src.player import Player
from src.card_pile import CardPile, PlayCardPile
from src.controller import Controller


class PlayerAction(ABC):
    @abstractmethod
    def is_valid(self, board: Board, player_index: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _get_arguments_from_user(self, board: Board, controller: Controller) -> tuple[Any]:
        raise NotImplementedError

    @abstractmethod
    def __call__(self, board: Board) -> None:
        raise NotImplementedError

    def name(self):
        return self.__class__.__name__


class PickUpPlayPile(PlayerAction):
    def is_valid(self, board: Board, player_index: int) -> bool:
        if board.player_index != player_index:
            return False
        return len(board.play_pile) > 0

    def _get_arguments_from_user(self, board: Board, controller: Controller) -> tuple[Any]:
        return tuple()

    def __call__(self, board: Board) -> None:
        player = board.player_index


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

    def get_player(self, player_index: int) -> Player:
        return self.players[player_index]

    def increment_player_index(self, increment: int=1) -> None:
        self.player_index += increment

    def play_card(self, card: Card) -> None:
        self.play_pile.add_card(card)

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
        self.increment_player_index(self.effect_multiplier)
        return None

    def __play_ten(self) -> None:
        self.effect_multiplier = 1
        self.play_order = 1 - self.play_order
        self.burn(is_joker=False)
        return None

    def __play_jack(self) -> None:
        if len(self.play_pile) <= 1:
            return None
        self.play_card(self.play_pile[-2])
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
        self.burn_pile.add_card(self.play_pile[-1])
        self.burn(is_joker=True)

        index = -1
        while not (0 <= index <= len(self.players)):
            index = input("Who would you like to be JOKERED? ")

        self.players[index].pickup(self.play_pile)
        return None

    def burn(self, is_joker: bool) -> None:
        if is_joker:
            self.burn_pile.add_card(self.burn_pile.pop())
            return None
        self.burn_pile.add_cards(self.play_pile)
        self.play_pile.clear()
        self.increment_player_index(-1)
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
