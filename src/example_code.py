from src.game import Game
from src.board_printer import BoardPrinter, BoardPrinterDebug


def main():
    # game = Game(4, board_printer=BoardPrinter)
    game = Game(4, board_printer=BoardPrinter)
    game.mulligan_all()
    game.choose_start_direction()
    game.play()


if __name__ == "__main__":
    main()
