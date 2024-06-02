from src.utils.printing import colour_blue, colour_green, colour_warning, colour_cyan, print_top_and_bottom_rows

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
                          f"Game State: ({self._repr_game_info(board)})")

        print("\n".join(_repr_players(board, select_index)) + game_state_str)
        return None

    def print_choosable_cards(self) -> None:
        print(f"Legal moves from {self.board.current_player.playable_cards}:")
        print(self.board.current_legal_combos)
        return None

    @staticmethod
    def _repr_game_info(board: IBoard):
        return (f"{board.play_order}, {board.turn_order}, Flipped?: {board.cards_are_flipped}, "
                f"Multiplier: {board.effect_multiplier}, Whose turn?: {board.player_index}, "
                f"#turns played: {board.turns_played}, burned this turn?: {board.has_burned_this_turn}")


class BoardPrinterDebug(IBoardPrinter):
    def __init__(self, board: IBoard):
        self.board = board

    @print_top_and_bottom_rows
    def print(self, select_index: int = None) -> None:
        board = self.board
        game_state_str = (f"Draw Pile: {board.draw_pile}\n"
                          f"Play Pile: {board.play_pile}\n"
                          f"Burn Pile: {board.burn_pile}\n"
                          f"Game State: ({self._repr_game_info(board)})")

        print("\n".join(_repr_players(board, select_index, debug=True)) + f"\nCombo Timeline: {board.combo_history}\n" + game_state_str)
        return None

    def print_choosable_cards(self) -> None:
        print(f"Legal moves from {self.board.current_player.playable_cards}:")
        print(self.board.current_legal_combos)
        return None

    @staticmethod
    def _repr_game_info(board: IBoard):
        return (f"{board.play_order}, {board.turn_order}, Flipped?: {colour_warning(board.cards_are_flipped)}, "
                f"Multiplier: {board.effect_multiplier}, Whose turn?: {board.player_index}, "
                f"#turns played: {board.turns_played}, burned this turn?: {board.has_burned_this_turn}")


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
    players_str = [f"{x} {i}" for x, i in enumerate(players_str)]
    return players_str


def __players_repr_debug(board: IBoard) -> list[str]:
    return [player.repr_debug() for i, player in enumerate(board.players)]


def __players_flipped_repr(board: IBoard, select_index: int) -> list[str]:
    return [player.__repr__() if i != select_index else player.repr_invisible_hand() for i, player in enumerate(board.players)]


def __players_repr(board: IBoard, select_index: int) -> list[str]:
    return [player.__repr__() if i == select_index else player.repr_invisible_hand() for i, player in enumerate(board.players)]
