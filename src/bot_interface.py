from abc import ABC, abstractmethod

from src.board_interface import BoardTurnOrder


class IBot(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def delay(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def action(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def card_play_indices(self) -> list[int]:
        raise NotImplementedError

    @property
    @abstractmethod
    def card_giveaway_index(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def card_giveaway_player_index(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def joker_target_index(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def wants_to_mulligan(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def mulligan_hand_index(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def mulligan_fuk_index(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def preferred_start_direction(self) -> BoardTurnOrder:
        raise NotImplementedError

    @property
    @abstractmethod
    def vote_for_winner_index(self) -> int:
        raise NotImplementedError


class BotNotReadyError(Exception):
    def __init__(self, bot: IBot):
        message = f"Board has not been set for \'{bot.name}\'"
        super().__init__(message)
