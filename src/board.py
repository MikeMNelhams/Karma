from __future__ import annotations

from typing import Iterable, Deque, Callable

from collections import deque

from src.utils.multiset import FrozenMultiset
from src.card_combo_permuations import equal_subsequence_permutations_with_filler, equal_subsequence_permutations_with_filler_and_filter
from src.cards import Cards, Card, CardValue
from src.player import Player
from src.card_pile import CardPile, PlayCardPile
from src.card_combos import CardComboFactory, Combo_3
from src.board_interface import BoardPlayOrder, BoardTurnOrder, IBoard, IBoardPrinter
from src.controller import Controller


type OnEndTurnEvent = Callable[[Board], None]


class Board(IBoard):

    INVALID_ACTIONS = {"draw_card", "receive_card", "rotate_hand"}

    __playable_card_comparisons = {BoardPlayOrder.UP: lambda x, y: x >= y, BoardPlayOrder.DOWN: lambda x, y: x <= y}
    __always_legal_cards_values = {CardValue.FOUR, CardValue.TWO}
    __filler_card = CardValue.SIX

    def __init__(self, players: Iterable[Player], draw_pile: CardPile | None=None,
                 burn_pile: CardPile | None=None, play_pile: PlayCardPile | None=None,
                 play_order: BoardPlayOrder = BoardPlayOrder.UP, turn_order: BoardTurnOrder = BoardTurnOrder.RIGHT,
                 cards_are_flipped: bool = False, effect_multiplier: int = 1, who_starts: int = 0,
                 has_burned_this_turn: bool = False, turns_played: int = 0):
        self._players = deque(players)
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
        self._player_index = who_starts
        self._has_burned_this_turn = has_burned_this_turn
        self._turns_played = turns_played

        self.__on_end_turn_events: list[OnEndTurnEvent] = []
        self.__card_combo_factory = CardComboFactory()
        self._has_burned_this_turn = False

        self.__current_legal_combos: set[Cards] = set()
        self.player_index_who_started_turn = who_starts

        self.__number_of_jokers_in_play = self.__count_in_play_jokers()

        self._combo_history = []

    def get_player(self, player_index: int) -> Player:
        return self.players[player_index]

    @property
    def current_player(self) -> Player:
        return self.get_player(self.player_index)

    def step_player_index(self, number_of_steps: int) -> None:
        self._player_index += self.turn_order.value * number_of_steps
        self._player_index %= len(self.players)
        return None

    def flip_turn_order(self) -> None:
        if self._turn_order == BoardTurnOrder.RIGHT:
            self._turn_order = BoardTurnOrder.LEFT
        else:
            self._turn_order = BoardTurnOrder.RIGHT
        return None

    def reset_play_order(self) -> None:
        self._play_order = BoardPlayOrder.UP
        return None

    def flip_play_order(self) -> None:
        if self._play_order == BoardPlayOrder.UP:
            self._play_order = BoardPlayOrder.DOWN
        else:
            self._play_order = BoardPlayOrder.UP
        return None

    def flip_hands(self) -> None:
        self._cards_are_flipped = not self.cards_are_flipped
        return None

    def start_turn(self) -> None:
        self.player_index_who_started_turn = self.player_index
        self._has_burned_this_turn = False
        self.__calculate_legal_combos(self.current_player.playable_cards)
        return None

    def end_turn(self) -> None:
        self._turns_played += 1
        self.__trigger_on_end_turn_events()
        return None

    def register_on_end_turn_event(self, on_end_turn_event: OnEndTurnEvent) -> None:
        self.__on_end_turn_events.append(on_end_turn_event)
        return None

    def __trigger_on_end_turn_events(self) -> None:
        for event in self.__on_end_turn_events:
            event(self)
        return None

    def play_cards(self, cards: Cards,
                   controller: Controller | None = None,
                   board_printer: IBoardPrinter | None = None) -> bool:
        """ Assumes the cards are a legal combo AND can legally be played."""
        self.play_pile.add_cards(cards)
        self.__draw_until_full()
        self.card_combo_factory.set_counts(cards)
        combo = self.card_combo_factory.create_combo(cards, controller=controller, board_printer=board_printer)
        combo(self)

        if combo.__class__.__name__ != Combo_3.__name__:
            self.set_effect_multiplier(1)

        self._combo_history.append(cards)
        return True

    def burn(self, joker_count: int) -> None:
        if joker_count > 0:
            cards_to_burn = self.play_pile.pop_multiple(list(range(len(self.play_pile) - joker_count, len(self.play_pile))))
            self.set_number_of_jokers_in_play(self.number_of_jokers_in_play - cards_to_burn.count_value(CardValue.JOKER))
            self.burn_pile.add_card(cards_to_burn)
            self._has_burned_this_turn = True
            return None
        self.burn_pile.add_cards(self.play_pile)
        self.play_pile.clear()
        self._has_burned_this_turn = True
        return None

    def is_legal_play(self, cards: Cards) -> bool:
        self.__card_combo_factory.set_counts(cards)
        if not self.__card_combo_factory.is_valid_combo():
            return False
        return cards.values in self.current_legal_combos

    def legal_combos_from_cards(self, cards: Cards) -> set[list[CardValue]]:
        if not cards:
            return set()

        if self.cards_are_flipped:
            return set(FrozenMultiset([card.value]) for card in cards)

        if not self.play_pile or self.play_pile.visible_top_card is None:
            return equal_subsequence_permutations_with_filler_and_filter(cards, CardValue.SIX, self.__is_joker, 3)

        top_card: Card = self.play_pile.visible_top_card
        comparison = self.__playable_card_comparisons[self.play_order]
        valid_cards = Cards(card for card in cards if card.value in self.__always_legal_cards_values or comparison(card, top_card))
        if top_card.value == CardValue.ACE:
            return equal_subsequence_permutations_with_filler(valid_cards, CardValue.SIX, 3)
        return equal_subsequence_permutations_with_filler_and_filter(valid_cards, CardValue.SIX, self.__is_joker, 3)

    def set_effect_multiplier(self, new_multiplier: int) -> None:
        self._effect_multiplier = new_multiplier
        return None

    def set_player_index(self, new_index: int) -> None:
        self._player_index = new_index
        self._player_index %= len(self.players)
        return None

    def __draw_until_full(self) -> None:
        if not self.draw_pile:
            return None

        player = self.current_player
        if len(player.hand) >= 3:
            return None
        for _ in range(3 - len(player.hand)):
            if not self.draw_pile:
                return None
            player.draw_card(self.draw_pile)
        return None

    @property
    def players(self) -> Deque[Player]:
        return self._players

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

    def set_turn_order(self, turn_order: BoardTurnOrder) -> None:
        self._turn_order = turn_order
        return None

    @property
    def cards_are_flipped(self) -> bool:
        return self._cards_are_flipped

    @property
    def effect_multiplier(self) -> int:
        return self._effect_multiplier

    @property
    def player_index(self) -> int:
        return self._player_index

    @property
    def has_burned_this_turn(self) -> bool:
        return self._has_burned_this_turn

    @property
    def turns_played(self) -> int:
        return self._turns_played

    @property
    def card_combo_factory(self) -> CardComboFactory:
        return self.__card_combo_factory

    @property
    def number_of_jokers_in_play(self) -> int:
        return self.__number_of_jokers_in_play

    def set_number_of_jokers_in_play(self, number_of_jokers: int) -> None:
        self.__number_of_jokers_in_play = number_of_jokers
        return None

    @property
    def combo_history(self) -> list[str]:
        return self._combo_history

    @property
    def current_legal_combos(self) -> set[list[CardValue]]:
        return self.__current_legal_combos

    @staticmethod
    def __is_joker(card: Card) -> bool:
        return card.value == CardValue.JOKER

    def __calculate_legal_combos(self, cards) -> None:
        self.__current_legal_combos = self.legal_combos_from_cards(cards)
        return None

    def __cards_possible_on_play_pile(self, test_cards: Cards, top_card: Card, comparison: Callable[[Card, Card], bool]) -> Cards:
        return Cards(card for card in test_cards if self.__is_always_valid(card) or comparison(card, top_card) or card.value == self.__filler_card)

    def __is_always_valid(self, card: Card) -> bool:
        return card in self.__always_legal_cards_values

    def __count_in_play_jokers(self) -> int:
        joker_count_in_draw_pile = self.draw_pile.count_value(CardValue.JOKER)
        joker_count_in_players = sum(player.number_of_jokers for player in self.players)
        return joker_count_in_draw_pile + joker_count_in_players
