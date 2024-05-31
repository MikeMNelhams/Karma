from typing import Iterable, Deque

from collections import deque

from src.board_interface import IBoardState, BoardPlayOrder, BoardTurnOrder

from src.card_pile import CardPile, PlayCardPile
from src.player import Player


class BoardState(IBoardState):
    def __init__(self, players: Iterable[Player], draw_pile: CardPile | None=None,
                 burn_pile: CardPile | None=None, play_pile: PlayCardPile | None=None,
                 play_order: BoardPlayOrder = BoardPlayOrder.UP, turn_order: BoardTurnOrder = BoardTurnOrder.RIGHT,
                 cards_are_flipped: bool = False, effect_multiplier: int = 1, who_starts: int = 0,
                 has_burned_this_turn: bool = False):
        self._players = players
        self._draw_pile = draw_pile
        if draw_pile is None:
            self._draw_pile = CardPile.empty()
        self._burn_pile = burn_pile
        if burn_pile is None:
            self._burn_pile = CardPile.empty()
        self._play_pile = play_pile
        if play_pile is None:
            self._play_pile = PlayCardPile.empty()
        self._play_order = play_order
        self._turn_order = turn_order
        self._cards_are_flipped = cards_are_flipped
        self._effect_multiplier = effect_multiplier
        self._who_starts = who_starts
        self._has_burned_this_turn = has_burned_this_turn

    @property
    def players(self) -> Deque[Player]:
        return deque(self._players)

    @property
    def draw_pile(self) -> CardPile:
        return self._draw_pile

    @property
    def burn_pile(self) -> CardPile:
        return self._burn_pile

    @property
    def play_pile(self) -> PlayCardPile:
        return self._play_pile

    @property
    def play_order(self) -> BoardPlayOrder:
        return self._play_order

    @property
    def turn_order(self) -> BoardTurnOrder:
        return self._turn_order

    @property
    def cards_are_flipped(self) -> bool:
        return self._cards_are_flipped

    @property
    def effect_multiplier(self) -> int:
        return self._effect_multiplier

    @property
    def player_index(self) -> int:
        return self._who_starts

    @property
    def has_burned_this_turn(self) -> bool:
        return self._has_burned_this_turn
