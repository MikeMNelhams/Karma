from __future__ import annotations

from abc import ABC, abstractmethod

from typing import Deque

from enum import Enum

from src.cards import Card, Cards, CardValue
from src.card_pile import CardPile, PlayCardPile
from src.player import Player
from src.controller import Controller


class BoardPlayOrder(Enum):
    UP = 0
    DOWN = 1


class BoardTurnOrder(Enum):
    LEFT = -1
    RIGHT = 1


class IBoard(ABC):
    @property
    @abstractmethod
    def players(self) -> Deque[Player]:
        raise NotImplementedError

    @property
    @abstractmethod
    def draw_pile(self) -> CardPile:
        raise NotImplementedError

    @property
    @abstractmethod
    def burn_pile(self) -> CardPile:
        raise NotImplementedError

    @property
    @abstractmethod
    def play_pile(self) -> PlayCardPile:
        raise NotImplementedError

    @property
    @abstractmethod
    def play_order(self) -> BoardPlayOrder:
        raise NotImplementedError

    @property
    @abstractmethod
    def turn_order(self) -> BoardTurnOrder:
        raise NotImplementedError

    @property
    @abstractmethod
    def cards_are_flipped(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def effect_multiplier(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def player_index(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def has_burned_this_turn(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def current_player(self) -> Player:
        raise NotImplementedError

    @abstractmethod
    def flip_turn_order(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def flip_play_order(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def flip_hands(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def end_turn(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def play_cards(self, cards: Cards,
                   controller: Controller | None = None,
                   board_printer: IBoardPrinter | None = None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def burn(self, *args) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_legal_play(self, play_card: Card) -> bool:
        raise NotImplementedError

    @abstractmethod
    def reset_play_order(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_effect_multiplier(self, new_multiplier: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_player_index(self, new_index: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def step_player_index(self, number_of_steps: int) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def number_of_jokers_in_play(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def set_number_of_jokers_in_play(self, number_of_jokers: int) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def game_info_repr(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def current_legal_combos(self) -> set[list[CardValue]]:
        raise NotImplementedError


class IBoardPrinter(ABC):
    @abstractmethod
    def __init__(self, board: IBoard):
        raise NotImplementedError

    @abstractmethod
    def print(self, select_index: int=None) -> None:
        raise NotImplementedError