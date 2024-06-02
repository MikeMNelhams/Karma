from src.game import Game
from src.board import Board
from src.board_printer import BoardPrinter, BoardPrinterDebug, BoardPrinterNone
from src.controllers import BotController
from src.bots import IntegrationTestBot
from src.board_seeds import BoardFactory


def main():
    start_board = BoardFactory(Board).random_start(number_of_players=4)
    bot = IntegrationTestBot("Bill", delay=0)
    bot.set_board(start_board)
    controller = BotController(bot)
    game = Game(start_board, board_printer=BoardPrinter, controller=controller)
    game.mulligan_all()
    game.choose_start_direction()
    game.play()


if __name__ == "__main__":
    main()
