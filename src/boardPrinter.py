from src.utils.printing import colour_blue

from typing import Iterable

from board import Board


class BoardPrinter:
    def __init__(self, board: Board):
        self.board = board

    def print(self) -> None:
        board = self.board
        game_state_str = (f"Draw Pile: {board.draw_pile}\n"
                          f"Play Pile: {board.play_pile}\n"
                          f"Burn Pile: {board.burn_pile}\n"
                          f"Game State: ({board.play_order}, Flipped?: {board.cards_are_flipped}"
                          f"Multiplier: {board.effect_multiplier}, whose turn: {board.player_index})")
        print("\n".join(self.__repr_players()) + "\n" + game_state_str)
        return None

    def __players_invisible(self) -> list[str]:
        return [player.repr_invisible_hand() for player in self.board.players]

    def __players_visible(self) -> list[str]:
        return [player.__repr__() for player in self.board.players]

    def __repr_players(self) -> Iterable[str]:
        board = self.board
        player_str = ""

        if board.cards_are_flipped:
            player_str = self.__players_invisible()
        else:
            player_str = self.__players_visible()
        return (colour_blue(x) if i == board.player_index else x for i, x in enumerate(player_str))
