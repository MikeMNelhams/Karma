from __future__ import annotations

from abc import ABC, abstractmethod

from collections import Counter, deque

from src.cards import Cards, CardValue, non_six_value
from src.hand import Hand
from src.player import Player
from src.board_interface import IBoard, IBoardPrinter
from src.controller_interface import IController
from prompt_manager import PromptManager
import src.response_conditions as rc

type CardValueCounts = dict[CardValue, int]


class CardCombo(ABC):
    def __init__(self, cards: Cards, counts: CardValueCounts,
                 controller: IController | None = None,
                 board_printer: IBoardPrinter | None = None,
                 prompt_manager: PromptManager | None = None):
        self.cards = cards
        self.controller = controller
        self.board_printer = board_printer
        self.__counts = counts
        self.prompt_manager = prompt_manager
        if prompt_manager is None:
            self.prompt_manager = PromptManager()

    def __len__(self) -> int:
        return len(self.cards)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.cards})"

    @abstractmethod
    def __call__(self, board: IBoard) -> None:
        raise NotImplementedError


class Combo_2(CardCombo):
    def __call__(self, board: IBoard) -> None:
        board.reset_play_order()
        return None


class Combo_3(CardCombo):
    def __call__(self, board: IBoard) -> None:
        board.set_effect_multiplier(board.effect_multiplier * (2 ** len(self)))
        return None


class Combo_4(CardCombo):
    def __call__(self, board: IBoard) -> None:
        return None


class Combo_5(CardCombo):
    def __call__(self, board: IBoard) -> None:
        hands = deque([player.hand for player in board.players])
        number_of_repeats = len(self) * board.effect_multiplier
        if number_of_repeats < len(board.players):
            self.__hand_rotates(board, hands, number_of_repeats)
            return None
        self.__hand_rotates(board, hands, len(board.players))
        self.__hand_rotates(board, hands, number_of_repeats % len(board.players))
        return None

    @staticmethod
    def __hand_rotates(board: IBoard, hands: deque[Hand], number_of_rotations: int) -> None:
        for _ in range(number_of_rotations):
            hands.rotate(1 * board.turn_order.value)
            for i in range(len(board.players)):
                board.players[i].hand = hands[i]
        return None


class Combo_6(CardCombo):
    def __call__(self, board: IBoard) -> None:
        return None


class Combo_7(CardCombo):
    def __call__(self, board: IBoard) -> None:
        if board.effect_multiplier & 1 == 0:
            return None
        board.flip_play_order()
        return None


class Combo_8(CardCombo):
    def __call__(self, board: IBoard) -> None:
        if board.effect_multiplier & 1 == 0:
            return None
        board.flip_turn_order()
        return None


class Combo_9(CardCombo):
    def __call__(self, board: IBoard) -> None:
        if board.play_pile.contains_min_length_run(4):
            return None
        number_of_repeats = len(self) * board.effect_multiplier
        board.step_player_index(number_of_repeats)
        return None


class Combo_10(CardCombo):
    def __call__(self, board: IBoard) -> None:
        board.burn(joker_count=0)
        return None


class Combo_Jack(CardCombo):
    def __call__(self, board: IBoard) -> None:
        if len(board.play_pile) <= len(self.cards):
            return None

        card_below_combo = board.play_pile[-1 - len(self)]
        if card_below_combo.value == CardValue.JACK:
            return None

        number_of_repeats = len(self) * board.effect_multiplier
        if card_below_combo.value == CardValue.THREE:
            number_of_repeats = len(self)  # Otherwise it would go 2 -> 8, which would errr, not be good
        board.play_cards(Cards.repeat(card_below_combo, number_of_repeats),
                         controller=self.controller, board_printer=self.board_printer,
                         add_to_play_pile=False)
        return None


class Combo_Queen(CardCombo):
    def __call__(self, board: IBoard) -> None:
        current_player = board.current_player
        if not current_player.has_cards:
            return None
        if current_player.playing_from == 1 and not current_player.karma_face_up:
            return None

        number_of_repeats = len(self) * board.effect_multiplier
        playing_index_at_start_of_combo = current_player.playing_from
        for _ in range(number_of_repeats):
            self.board_printer.print(board.player_index)
            if current_player.playing_from != playing_index_at_start_of_combo:
                return None
            if current_player.playable_cards.is_exclusively(CardValue.JOKER):
                return None
            self.__give_away_card(board, current_player)
            if not current_player.has_cards:
                return None
        return None

    def __give_away_card(self, board: IBoard, current_player):
        joker_indices = {i for i, card in enumerate(current_player.playable_cards) if card.value == CardValue.JOKER}
        card_index_selected = self.controller.get_response([self.prompt_manager["give_away"]],
                                                           [rc.IsNumberSelection(0,
                                                                                 len(current_player.playable_cards) - 1,
                                                                                 1,
                                                                                 exclude=joker_indices)])
        excluded_target_players = board.potential_winner_indices | {board.player_index}
        target_player_index = self.controller.get_response([self.prompt_manager["give_away_select_player"]],
                                                           [rc.IsNumberSelection(0,
                                                                                 len(board.players) - 1,
                                                                                 1,
                                                                                 exclude=excluded_target_players)])
        target_player: Player = board.players[target_player_index[0]]
        target_player.receive_card(current_player.playable_cards.pop(card_index_selected[0]))
        if board.draw_pile and len(current_player.hand) < 3:
            current_player.draw_card(board.draw_pile)
        return None


class Combo_King(CardCombo):
    def __call__(self, board: IBoard) -> None:
        number_of_repeats = len(self) * board.effect_multiplier

        if board.play_pile.contains_min_length_run(4):
            board.burn(joker_count=0)

        number_of_repeats = min(number_of_repeats, len(board.burn_pile))
        if number_of_repeats == 0:
            return None
        cards_to_play = board.burn_pile.remove_from_bottom(number_of_repeats)
        for card in cards_to_play:
            if card.value == CardValue.JOKER:
                board.set_number_of_jokers_in_play(board.number_of_jokers_in_play + 1)
            board.play_cards(Cards([card]), controller=self.controller, board_printer=self.board_printer)
        return None


class Combo_Ace(CardCombo):
    def __call__(self, board: IBoard) -> None:
        number_of_repeats = len(self) * board.effect_multiplier
        if number_of_repeats == 1:
            board.flip_hands()
            if board.cards_are_flipped:
                for player in board.players:
                    if player.hand:
                        player.hand.shuffle()
            elif not board.cards_are_flipped:
                for player in board.players:
                    if player.hand:
                        player.hand.sort()
            return None
        board.flip_hands()
        board.flip_hands()
        return None


class Combo_Joker(CardCombo):
    def __call__(self, board: IBoard) -> None:
        board.burn(joker_count=len(self))
        current_player_index = board.player_index
        target_index = self.controller.get_response([self.prompt_manager["joker_select_player"]],
                                                    [rc.IsNumberSelection(0, len(board.players) - 1,
                                                                          max_selection_count=1,
                                                                          exclude=current_player_index)])
        target_index = target_index[0]
        board.players[target_index].pickup(board.play_pile)
        return None


class CardComboFactory:
    combo_maps: dict[CardValue, CardCombo] = {CardValue.TWO: Combo_2, CardValue.THREE: Combo_3,
                                              CardValue.FOUR: Combo_4, CardValue.FIVE: Combo_5,
                                              CardValue.SIX: Combo_6, CardValue.SEVEN: Combo_7,
                                              CardValue.EIGHT: Combo_8, CardValue.NINE: Combo_9,
                                              CardValue.TEN: Combo_10, CardValue.JACK: Combo_Jack,
                                              CardValue.QUEEN: Combo_Queen, CardValue.KING: Combo_King,
                                              CardValue.ACE: Combo_Ace, CardValue.JOKER: Combo_Joker}

    def __init__(self, prompt_file_path: str = "prompts.csv"):
        self.__counts = {}
        self.__prompt_manager = PromptManager(prompt_file_path)
        self.__cards = None

    def is_valid_combo(self) -> bool:
        counts = self.__counts
        if len(counts) > 2:
            return False
        if len(counts) == 2:
            return CardValue.SIX in counts
        return True

    def set_counts(self, cards: Cards) -> None:
        self.__counts = self.__calculate_counts(cards)
        self.__cards = cards
        return None

    def create_combo(self, controller: IController | None = None,
                     board_printer: IBoardPrinter | None = None) -> CardCombo:
        card_value = self.major_card_value()
        card_combo_class = self.combo_maps[card_value]
        return card_combo_class(self.__cards, self.__counts,
                                controller=controller,
                                board_printer=board_printer,
                                prompt_manager=self.__prompt_manager)

    def combo_visibility(self, board: IBoard) -> list[int]:
        card_value = self.major_card_value()
        if card_value == CardValue.FOUR:
            combo_visibility = [0 for _ in range(len(self.__cards))]
        elif card_value == CardValue.JACK:
            visibility = 1
            if board.play_pile and board.play_pile[-1].value == CardValue.FOUR:
                visibility = 0
            combo_visibility = [visibility for _ in range(len(self.__cards))]
        else:
            combo_visibility = [1 for _ in range(len(self.__cards))]
        return combo_visibility

    def major_card_value(self) -> CardValue:
        if len(self.__counts) == 1:
            return list(self.__counts.keys())[0]
        elif len(self.__counts) == 2:
            return non_six_value(self.__counts)
        raise TypeError("Too many different type cards!")

    @staticmethod
    def __calculate_counts(cards: Cards) -> dict[CardValue, int]:
        return Counter(card.value for card in cards)
