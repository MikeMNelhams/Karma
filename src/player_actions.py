from __future__ import annotations

from abc import ABC, abstractmethod

from typing import Callable

from src.cards import Cards
from src.board_interface import IBoard, IBoardPrinter
from src.controller import Controller


type CardGetter = Callable[[], Cards]


class PlayerAction(ABC):
    @abstractmethod
    def is_valid(self, board: IBoard) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __call__(self, board: IBoard, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def copy(self):
        raise NotImplementedError

    def name(self):
        return self.__class__.__name__


class PickUpPlayPile(PlayerAction):
    def is_valid(self, board: IBoard) -> bool:
        if not board.current_player.has_cards:
            return False
        return len(board.play_pile) > 0

    def __call__(self, board: IBoard, **kwargs) -> None:
        player = board.current_player
        player.pickup(board.play_pile)
        return None

    def copy(self):
        return PickUpPlayPile()


class PlayCardsCombo(PlayerAction):
    def __init__(self, cards_getter: CardGetter):
        self.__cards_getter = cards_getter
        self.__cards = None

    @property
    def cards(self) -> Cards:
        if self.__cards is None:
            self.__get_cards()
        return self.__cards

    def __get_cards(self) -> None:
        self.__cards = self.__cards_getter()
        return None

    def is_valid(self, board: IBoard) -> bool:
        if not board.current_player.has_cards:
            return False
        return len(board.current_legal_combos) > 0

    def __call__(self, board: IBoard, controller: Controller = None, board_printer: IBoardPrinter | None = None) -> None:
        player = board.current_player

        while self.cards is None or self.cards.values not in board.current_legal_combos:
            self.__get_cards()
        cards_to_play = player.playable_cards.remove(self.cards)
        print(f"Selected VALID cards to play: {cards_to_play}")
        board.play_cards(cards_to_play, controller, board_printer)
        return None

    def copy(self):
        return PlayCardsCombo(cards_getter=self.__cards_getter)
