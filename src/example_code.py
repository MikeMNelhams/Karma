from src.game import Game
from src.board import Board
from src.board_printer import BoardPrinter, BoardPrinterDebug
from src.board_seeds import BoardFactory


def main():
    start_board = BoardFactory(Board).random_start(number_of_players=4)
    game = Game(start_board, board_printer=BoardPrinterDebug)
    game.mulligan_all()
    game.choose_start_direction()
    game.play()


if __name__ == "__main__":
    main()
