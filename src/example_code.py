from src.game import Game
from src.board import Board
from src.board_printer import BoardPrinter, BoardPrinterDebug
from src.board_seeds import BoardFactory


def main():
    p0 = [[2, 3, 4], [5, 6, 7], [8, 9, 10]]
    p1 = [[11, 12, 13, 14], [15], []]
    p2 = [[], [], []]
    p3 = [[], [], []]
    player_matrix = [p0, p1, p2, p3]
    start_board = BoardFactory(Board).matrix_start(player_matrix, [2, 3, 5, 7])

    # start_board = BoardFactory(Board).random_start(number_of_players=4)
    game = Game(start_board, board_printer=BoardPrinterDebug)
    game.mulligan_all()
    game.choose_start_direction()
    game.play()


if __name__ == "__main__":
    main()
