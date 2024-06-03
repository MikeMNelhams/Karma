from __future__ import annotations

from typing import Callable

from src.utils.multiset import FrozenMultiset

from src.cards import Cards
from src.board_interface import IBoard, IBoardPrinter, IAction
from src.controller_interface import IController


type CardGetter = Callable[[], Cards]


class PickUpPlayPile(IAction):
    @classmethod
    def name(cls) -> str:
        return "pickup"

    @classmethod
    def is_valid(cls, board: IBoard) -> bool:
        if not board.current_player.has_cards:
            return False
        return len(board.play_pile) > 0

    def __call__(self, board: IBoard, **kwargs) -> None:
        player = board.current_player
        player.pickup(board.play_pile)
        board.set_effect_multiplier(1)
        return None

    def copy(self):
        return PickUpPlayPile()


class PlayCardsCombo(IAction):
    @classmethod
    def name(cls) -> str:
        return "play_cards"

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

    @classmethod
    def is_valid(cls, board: IBoard) -> bool:
        if not board.current_player.has_cards:
            return False
        return len(board.current_legal_combos) > 0

    def __call__(self, board: IBoard, controller: IController = None, board_printer: IBoardPrinter | None = None) -> None:
        player = board.current_player

        while self.cards is None or FrozenMultiset(self.cards.values) not in board.current_legal_combos:
            self.__get_cards()
        cards_to_play = player.playable_cards.remove(self.cards)
        board.play_cards(cards_to_play, controller=controller, board_printer=board_printer)
        return None

    def copy(self):
        return PlayCardsCombo(cards_getter=self.__cards_getter)
