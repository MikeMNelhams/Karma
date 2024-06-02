from bot_interface import IBot

from src.cards import CardValue
from src.utils.multiset import FrozenMultiset
from src.board_interface import IBoard, BoardTurnOrder
from src.board_actions import PickUpPlayPile, PlayCardsCombo


class IntegrationTestBot(IBot):
    """ Inputs are randomised. This is only for testing. It is not a GOOD bot"""

    def __init__(self, name: str, delay: float=0.5):
        self._name = name
        self.__board: IBoard | None = None
        self._delay = delay

    @property
    def delay(self) -> float:
        return self._delay

    def set_board(self, board: IBoard) -> None:
        self.__board = board

    @property
    def is_ready(self) -> bool:
        return self.__board is not None

    def name(self) -> str:
        return self._name

    def action(self) -> str:
        pickup_name = PickUpPlayPile.name()
        play_cards_name = PlayCardsCombo.name()
        if pickup_name in self.__board.current_legal_actions:
            return pickup_name
        return play_cards_name

    def card_play_indices(self) -> list[int]:
        legal_combos = self.__board.current_legal_combos
        playable_cards = self.__board.current_player.playable_cards
        legal_combo: FrozenMultiset = legal_combos.pop()

        legal_items = dict(legal_combo.items())

        indices = []
        # TODO Speedup using total count of values decreasing till 0 and break at 0
        for i, card in enumerate(playable_cards):
            value = card.value
            if value in legal_items and legal_items[value] > 0:
                legal_items[value] -= 1
                indices.append(i)
        return indices

    def card_giveaway_index(self) -> int:
        playable_cards = self.__board.current_player.playable_cards
        values = playable_cards.values
        legal_values = {i for i, value in enumerate(values) if value != CardValue.JOKER}
        return legal_values.pop()

    def card_giveaway_player_index(self) -> int:
        potential_winner_indices = self.__board.potential_winner_indices
        valid_indices = self.__other_player_indices - potential_winner_indices
        return valid_indices.pop()

    def joker_target_index(self) -> int:
        potential_winner_indices = self.__board.potential_winner_indices - {self.__board.player_index}
        if potential_winner_indices:
            return potential_winner_indices.pop()
        return self.__other_player_indices.pop()

    def wants_to_mulligan(self) -> str:
        return "n"

    def mulligan_hand_index(self) -> int:
        raise NotImplementedError

    def mulligan_fuk_index(self) -> int:
        raise NotImplementedError

    def preferred_start_direction(self) -> BoardTurnOrder:
        return BoardTurnOrder.RIGHT

    def vote_for_winner_index(self) -> int:
        vote = self.__board.potential_winner_indices.pop()
        return vote

    @property
    def __other_player_indices(self) -> set[int]:
        return {x for x in range(len(self.__board.players))} - {self.__board.player_index}
