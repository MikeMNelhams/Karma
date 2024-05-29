from src.player import Player
from src.cards import Card, Cards, CardValue, SUITS, CARD_VALUE_NAMES
from src.hand import Hand
from src.poop import PoopFaceDown, PoopFaceUp
from src.card_pile import CardPile
from src.board import Board
from src.boardPrinter import BoardPrinter
from src.controller import Controller
import src.response_conditions as rc


class Game:
    def __init__(self, number_of_players: int, number_of_jokers: int = 1, who_starts: int = 0):
        jokers = Cards(Card(SUITS[i % len(SUITS)], CardValue.JOKER) for i in range(number_of_jokers))
        deck = Cards(Card(SUITS[i], CardValue(j)) for j in range(2, 15) for i in range(len(SUITS)))
        deck.shuffle()

        face_down_poops = [PoopFaceDown(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2]))
                           for i in range(number_of_players)]
        deck.add_cards(jokers)
        del jokers
        deck.shuffle()
        face_up_poops = [PoopFaceUp(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2]))
                         for i in range(number_of_players)]
        hands = [Hand(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2])) for i in range(number_of_players)]

        players = [Player(h, fdp, fup) for h, fdp, fup in zip(hands, face_down_poops, face_up_poops)]
        draw_pile = CardPile(deck)

        self.board = Board(players, draw_pile, who_starts)
        self.boardPrinter = BoardPrinter(self.board)
        self.controller = Controller()

    def play_turn(self) -> None:
        self.print()

    def mulligan_all(self) -> None:
        for i in range(len(self.board.players)):
            self.print(i)
            self._mulligan_player(i)
            self.boardPrinter.clear_all_text()
        return None

    def _mulligan_player(self, player_index: int) -> None:
        current_player = self.board.get_player(player_index)
        user_wants_to_mulligan = self.controller.ask_user(["Would you like to mulligan? (Y/N)"],
                                                          [rc.IsYesOrNo()])[0] == "y"

        while user_wants_to_mulligan:
            mulligan_swap = self.controller.ask_user(
                ["Which HAND card index would you like to swap?", "Which FUP card index would you like to swap?"],
                [rc.IsWithinRange(0, 3), rc.IsWithinRange(0, 3)])
            current_player.swap_hand_card_with_poop(mulligan_swap[0], mulligan_swap[1])
            self.print(player_index)
            user_wants_to_mulligan = self.controller.ask_user(["Would you like to mulligan? (Y/N)"],
                                                              [rc.IsYesOrNo()])[0] == "y"
        return None

    def print(self, select_index: int=None) -> None:
        self.boardPrinter.print(select_index)


def main():
    game = Game(4)
    game.mulligan_all()


if __name__ == "__main__":
    main()
