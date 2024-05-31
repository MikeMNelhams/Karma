from collections import defaultdict

from src.cards import Cards
from src.board import Board
from src.board_state import BoardState
from src.board_interface import BoardTurnOrder
from src.board_printer import BoardPrinter, BoardPrinterDebug
from src.board_seeds import BoardFactory
from src.player_actions import PlayerAction, PlayCardsCombo, PickUpPlayPile
from src.controller import Controller
from src import response_conditions as rc


class GameWonException(Exception):
    def __init__(self, game_ranks: list[int]):
        message = f"Overall Rankings: {game_ranks}"
        super().__init__(message)


class GameTurnLimitExceededException(Exception):
    def __init__(self, game_ranks: list[int], turn_limit: int):
        message = f"Max turn limit of {turn_limit} has been hit!\nPlayer {game_ranks[0]} wins!\nOverall Rankings: {game_ranks}"
        super().__init__(message)


class Game:
    def __init__(self, number_of_players: int, number_of_jokers: int = 1, who_starts: int = 0, turn_limit: int = 100,
                 board_printer=BoardPrinter):
        self.turn_limit = turn_limit
        self.board: Board = BoardFactory(BoardState, Board).random_start(number_of_players, number_of_jokers, who_starts)
        self.boardPrinter = board_printer(self.board)
        self.controller = Controller()

        self.game_ranks = {i: len(player) for i, player in enumerate(self.board.players)}

        self.board.register_on_end_turn_event(self.__step_one_turn)  # Try to step a turn first
        self.board.register_on_end_turn_event(self.__play_turn_again_if_burned_this_turn)  # Get another go if burned
        self.board.register_on_end_turn_event(self.__check_if_winner)  # Raise an exception if game-end condition met

        self.__possible_actions: dict[str, PlayerAction] = {"pickup": PickUpPlayPile(),
                                                            "play_cards": PlayCardsCombo(self.__card_selection_getter)}
        self.__number_of_jokers = number_of_jokers

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
                ["Which HAND card index would you like to swap?", "Which FUK card index would you like to swap?"],
                [rc.IsWithinRange(0, 3), rc.IsWithinRange(0, 2)])
            player.swap_hand_card_with_karma(mulligan_swap[0], mulligan_swap[1])
            self.print(player_index)
            user_wants_to_mulligan = self.controller.ask_user(["Would you like to mulligan? (Y/N)"],
                                                              [rc.IsYesOrNo()])[0] == "y"
        return None

    def choose_start_direction(self) -> None:
        self.print(self.board.player_index)
        direction = self.controller.ask_user(["Which direction do you want to go? (<--- L or R --->)"],
                                             [rc.IsInSet({"l", "r"})])
        if direction[0].lower() == "r":
            return self.board.set_turn_order(BoardTurnOrder.RIGHT)
        self.board.set_turn_order(BoardTurnOrder.LEFT)
        return None

    def play_turn(self) -> None:
        self.print(self.board.player_index)

        self.board.start_turn()

        actions = self.__possible_actions.copy()
        print(f"Legal moves from {self.board.current_player.playable_cards}:")
        print(self.board.current_legal_combos)
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
                                                   [rc.IsInSet(set(action_names))])[0]

        action: PlayerAction = self.__possible_actions[action_name].copy()
        action(self.board, controller=self.controller, board_printer=self.boardPrinter)
        self.board.end_turn()
        return None

    def play(self) -> None:
        for _ in range(self.turn_limit * len(self.board.players) + 1):
            self.play_turn()
        return None

    @property
    def number_of_potential_winners(self) -> int:
        return sum(1 if len(player) == 0 else 0 for player in self.board.players)

    def __card_selection_getter(self) -> Cards:
        lower_bound = 0
        upper_bound = len(self.board.current_player.playable_cards) - 1
        max_selection = len(self.board.current_player.playable_cards)
        prompt = f"What card indices do you want to play? From[{lower_bound}, {upper_bound}] - Pick up to {max_selection}"
        card_indices_selected = self.controller.ask_user([prompt],
                                                         [rc.IsNumberSelection(lower_bound,
                                                                               upper_bound,
                                                                               max_selection)])
        selected_cards = self.board.current_player.playable_cards.get(card_indices_selected[0])
        return selected_cards

    def __play_turn_again_if_burned_this_turn(self, board: Board) -> None:
        if not board.get_player(board.player_index_who_started_turn).has_cards:
            return None
        if board.has_burned_this_turn:
            board.set_player_index(board.player_index_who_started_turn)
            self.play_turn()
        return None

    @staticmethod
    def __step_one_turn(board: Board) -> None:
        board.step_player_index(1)
        return None

    def __check_if_winner(self, board: Board) -> None:
        self.__update_game_ranks(board)
        number_of_potential_winners = self.number_of_potential_winners
        if number_of_potential_winners == 1 and board.number_of_jokers_in_play == 0:
            raise GameWonException(self.game_ranks)

        if number_of_potential_winners == 2:
            if board.number_of_jokers_in_play == 0:
                raise GameWonException(self.game_ranks)

            votes = defaultdict(int)
            joker_counts = {}
            for player_index, player in enumerate(board.players):
                joker_count = board.get_player(player_index).number_of_jokers
                if joker_count > 0:
                    joker_counts[player_index] = joker_count
            potential_winners_indices = self.game_ranks[0]
            player_indices_to_exclude_from_vote = {x for x in range(len(board.players))} - potential_winners_indices
            for player_index, number_of_votes in joker_counts.items():
                board.set_player_index(player_index)
                player_vote = self.controller.ask_user([f"Hi player: {player_index}. Who do you want to win?"],
                                                       [rc.IsNumberSelection(0, len(board.players),
                                                                             max_selection_count=1,
                                                                             exclude=player_indices_to_exclude_from_vote)])
                votes[player_vote[0]] += number_of_votes
            print(f"Votes: {votes}")
            most_votes = max(votes.values())
            player_indices_with_most_votes = [player_index for player_index, count in votes.items() if count == most_votes]

            for player_index in player_indices_with_most_votes:
                self.game_ranks[player_index] = 0

            raise GameWonException(self.game_ranks)

        if number_of_potential_winners == len(board.players) - self.__number_of_jokers:
            raise GameWonException(self.game_ranks)

        if board.turns_played >= self.turn_limit:
            raise GameTurnLimitExceededException(self.game_ranks, self.turn_limit)

        return None

    def __update_game_ranks(self, board: Board) -> None:
        card_counts = defaultdict(set)
        for i, player in enumerate(board.players):
            card_counts[len(player)].add(i)

        ranks = [(card_count, player_indices) for card_count, player_indices in card_counts.items()]
        ranks.sort(key=lambda x: x[0])
        self.game_ranks = {}
        for rank, pair in enumerate(ranks):
            for player_index in pair[1]:
                self.game_ranks[player_index] = rank
        return None


def main():
    print("No longer the main, try running \'example_code.py\' instead!")


if __name__ == "__main__":
    main()
