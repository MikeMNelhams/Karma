from bot_interface import IBot
from src.board_interface import IBoard, BoardTurnOrder
from src.board_actions import IAction, PickUpPlayPile, PlayCardsCombo


class IntegrationTestBot(IBot):
    def __init__(self, name: str):
        super().__init__(name)
        self.__board: IBoard | None = None

    def set_board(self, board: IBoard) -> None:
        self.__board = board

    @property
    def is_ready(self) -> bool:
        return self.__board is not None

    def action(self) -> IAction:
        pass

    def card_play_indices(self) -> list[int]:
        pass

    def card_giveaway_index(self) -> int:
        pass

    def card_giveaway_player_index(self) -> int:
        pass

    def joker_target_index(self) -> int:
        pass

    def wants_to_mulligan(self) -> int:
        pass

    def mulligan_hand_index(self) -> int:
        pass

    def mulligan_fuk_index(self) -> int:
        pass

    def preferred_start_direction(self) -> BoardTurnOrder:
        pass

    def vote_for_winner_index(self) -> int:
        pass