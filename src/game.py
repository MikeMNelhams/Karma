from typing import Iterable

from src.player import Player
from src.cards import Card, Cards, CardValue, SUITS
from src.hand import Hand
from src.poop import PoopFaceDown, PoopFaceUp
from src.card_pile import CardPile
from src.board import Board
from src.board_printer import BoardPrinter
from src.player_actions import PlayerAction, PlayCardsCombo, PickUpPlayPile
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

        self.board.register_on_burn_listener(self.play_turn)  # You get another go after burning

        self.__possible_actions: dict[str, PlayerAction] = {"pickup": PickUpPlayPile(),
                                                            "play_cards": PlayCardsCombo(self.__card_selection_getter)}

    def mulligan_all(self) -> None:
        for i in range(len(self.board.players)):
            self.print(i)
            self._mulligan_player(i)
        return None

    def print(self, select_index: int=None) -> None:
        self.boardPrinter.print(select_index)
        return None

    def _mulligan_player(self, player_index: int) -> None:
        player = self.board.get_player(player_index)
        user_wants_to_mulligan = self.controller.ask_user(["Would you like to mulligan? (Y/N)"],
                                                          [rc.IsYesOrNo()])[0] == "y"

        while user_wants_to_mulligan:
            mulligan_swap = self.controller.ask_user(
                ["Which HAND card index would you like to swap?", "Which FUP card index would you like to swap?"],
                [rc.IsWithinRange(0, 3), rc.IsWithinRange(0, 2)])
            player.swap_hand_card_with_poop(mulligan_swap[0], mulligan_swap[1])
            self.print(player_index)
            user_wants_to_mulligan = self.controller.ask_user(["Would you like to mulligan? (Y/N)"],
                                                              [rc.IsYesOrNo()])[0] == "y"
        return None

    def choose_start_direction(self) -> None:
        self.print(self.board.player_index)
        direction = self.controller.ask_user(["Which direction do you want to go? (<--- L or R --->)"],
                                             [rc.IsInSet({"l", "r"})])
        if direction == "r":
            return None
        self.board.flip_turn_order()
        return None

    def play_turn(self) -> None:
        self.print(self.board.player_index)

        actions = self.__possible_actions.copy()
        for action_name in self.__possible_actions:
            if not actions[action_name].is_valid(self.board):
                actions.pop(action_name)

        if not actions:
            self.board.end_turn()
            self.print()
            return None

        action_names = [key for key in actions]

        if len(action_names) == 1:
            action_name = action_names[0]
        else:
            action_name = self.controller.ask_user([f"What action would you like to do: ({"/".join(action_names)})"],
                                                   [rc.IsInSet(set(action_names))])
        action = self.__possible_actions[action_name]
        action(self.board)
        self.print(self.board.player_index)
        raise NameError(f"The action name: {action_name} does not exist. Something wrong has occurred.")

    def play(self) -> None:
        for _ in range(8):
            self.play_turn()
        return None

    def __card_selection_getter(self) -> Cards:
        card_indices_selected = self.controller.ask_user(["What card indices do you want to play?"],
                                                         [rc.IsNumberSelection(0,
                                                                               len(self.board.current_player.playable_cards) - 1,
                                                                               len(self.board.current_player.playable_cards))])
        card_indices_selected = card_indices_selected[0]
        return self.board.current_player.playable_cards.get(card_indices_selected)


def main():
    game = Game(4)
    game.mulligan_all()
    game.choose_start_direction()
    game.play()



if __name__ == "__main__":
    main()
