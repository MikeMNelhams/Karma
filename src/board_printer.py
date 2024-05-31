from src.utils.printing import colour_blue, colour_green, colour_cyan, print_top_and_bottom_rows

from typing import Iterable

from board_interface import IBoard, IBoardPrinter


class BoardPrinter(IBoardPrinter):
    def __init__(self, board: IBoard):
        self.board = board

    @print_top_and_bottom_rows
    def print(self, select_index: int=None) -> None:
        board = self.board
        game_state_str = (f"Draw Pile: {board.draw_pile.repr_flipped()}\n"
                          f"Play Pile: {board.play_pile}\n"
                          f"Burn Pile: {board.burn_pile}\n"
                          f"Game State: ({board.game_info_repr})")
        print("\n".join(_repr_players(board, select_index)) + "\n" + game_state_str)
        return None


class BoardPrinterDebug(IBoardPrinter):
    def __init__(self, board: IBoard):
        self.board = board

    @print_top_and_bottom_rows
    def print(self, select_index: int = None) -> None:
        board = self.board
        game_state_str = (f"Draw Pile: {board.draw_pile}\n"
                          f"Play Pile: {board.play_pile}\n"
                          f"Burn Pile: {board.burn_pile}\n"
                          f"Game State: ({board.game_info_repr})")
        print("\n".join(_repr_players(board, select_index, debug=True)) + "\n" + game_state_str)
        return None


def _repr_players(board: IBoard, select_index: int=None, debug: bool=False) -> Iterable[str]:
    player_str = ""  # noqa

    if debug:
        player_str = __players_repr_debug(board)
    elif board.cards_are_flipped:
        player_str = __players_flipped_repr(board, select_index)
    else:
        player_str = __players_repr(board, select_index)
    players_str = [colour_cyan(x) if i == board.player_index and i == select_index else
                   (colour_green(x) if i == select_index else
                    (colour_blue(x) if i == board.player_index else x))
                   for i, x in enumerate(player_str)]
    return players_str


def __players_repr_debug(board: IBoard) -> list[str]:
    return [player.repr_debug() for i, player in enumerate(board.players)]


def __players_flipped_repr(board: IBoard, select_index: int) -> list[str]:
    return [player.__repr__() if i != select_index else player.repr_invisible_hand() for i, player in enumerate(board.players)]


def __players_repr(board: IBoard, select_index: int) -> list[str]:
    return [player.__repr__() if i == select_index else player.repr_invisible_hand() for i, player in enumerate(board.players)]