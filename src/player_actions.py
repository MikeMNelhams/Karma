from abc import ABC, abstractmethod

from typing import Callable

from src.cards import Cards
from src.board import Board

type CardGetter = Callable[[], Cards]


class PlayerAction(ABC):
    @abstractmethod
    def is_valid(self, board: Board) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __call__(self, board: Board) -> None:
        raise NotImplementedError

    def name(self):
        return self.__class__.__name__


class PickUpPlayPile(PlayerAction):
    def is_valid(self, board: Board) -> bool:
        if not board.current_player.has_cards:
            return False
        return len(board.play_pile) > 0

    def __call__(self, board: Board) -> None:
        player = board.current_player
        player.pickup(board.play_pile)
        return None


class PlayCardsCombo(PlayerAction):
    def __init__(self, cards_getter: CardGetter):
        self.__cards_getter = cards_getter
        self.__cards = None

    @property
    def cards(self) -> Cards:
        if self.__cards is None:
            self.__cards = self.__cards_getter()
        return self.__cards

    def is_valid(self, board: Board) -> bool:
        if not self.cards:
            return False

        player = board.current_player
        if not player.has_cards:
            return False

        if not player.playable_cards.contains(self.cards):
            return False

        return board.is_legal_play(self.cards[0])

    def __call__(self, board: Board) -> None:
        player = board.current_player
        board.play_cards(player.playable_cards.remove(self.cards))
        return None
