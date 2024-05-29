from src.utils.printing import colour_blue, colour_green, colour_cyan, print_row, clear_all_text

from typing import Iterable

from board import Board


class BoardPrinter:
    def __init__(self, board: Board):
        self.board = board

    def print(self, select_index: int=None) -> None:
        print_row()
        board = self.board
        game_state_str = (f"Draw Pile: {board.draw_pile}\n"
                          f"Play Pile: {board.play_pile}\n"
                          f"Burn Pile: {board.burn_pile}\n"
                          f"Game State: ({board.play_order}, Flipped?: {board.cards_are_flipped}"
                          f"Multiplier: {board.effect_multiplier}, whose turn: {board.player_index})")
        print("\n".join(self.__repr_players(select_index)) + "\n" + game_state_str)
        print_row()
        return None

    def __players_invisible(self) -> list[str]:
        return [player.repr_invisible_hand() for player in self.board.players]

    def __players_visible(self) -> list[str]:
        return [player.__repr__() for player in self.board.players]

    def __repr_players(self, select_index: int=None) -> Iterable[str]:
        board = self.board
        player_str = ""  # noqa

        if board.cards_are_flipped:
            player_str = self.__players_invisible()
        else:
            player_str = self.__players_visible()
        players_str = [colour_cyan(x) if i == board.player_index and i == select_index else (colour_green(x) if i == select_index else (colour_blue(x) if i == board.player_index else x)) for i, x in enumerate(player_str)]

        return players_str

    @staticmethod
    def clear_all_text() -> None:
        clear_all_text()
        return None
