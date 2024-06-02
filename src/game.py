from collections import defaultdict

from src.cards import Cards
from src.board import Board
from src.board_interface import BoardTurnOrder, IBoard, IAction, MetaIAction
from src.board_printer import BoardPrinter
from src.board_seeds import BoardFactory
from src.controller_interface import IController
from src.controllers import PlayerController
from src.prompt_manager import PromptManager
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
    def __init__(self, start_board: IBoard = None, turn_limit: int = 100,
                 board_printer=BoardPrinter, controller: IController=PlayerController()):
        self.turn_limit = turn_limit
        if start_board is None:
            self.board: Board = BoardFactory(Board).random_start(number_of_players=4)
        else:
            self.board = start_board
        self.controller = controller
        self.boardPrinter = board_printer(self.board)
        self.prompt_manager = PromptManager()

        self.game_ranks = {i: len(player) for i, player in enumerate(self.board.players)}

        self.board.register_on_end_turn_event(self.__step_one_turn)  # Try to step a turn first
        self.board.register_on_end_turn_event(self.__play_turn_again_if_burned_this_turn)  # Get another go if burned
        self.board.register_on_end_turn_event(self.__check_if_winner)  # Raise an exception if game-end condition met

    def play(self) -> None:
        for _ in range(self.turn_limit * len(self.board.players) + 1):
            self.play_turn()
        return None

    def play_turn(self) -> None:
        self.print(self.board.player_index)
        self.board.start_turn()

        self.boardPrinter.print_choosable_cards()  # Currently useful for debugging
        actions = self.board.current_legal_actions

        if not actions:
            self.board.end_turn()
            return None

        actions_map = {action.name(): action for action in actions}
        action_name = self.__get_action_name(actions)

        action_class: MetaIAction = actions_map[action_name]
        if action_name == "pickup":
            action: IAction = action_class()
        elif action_name == "play_cards":
            action: IAction = action_class(self.__card_selection_getter)
        else:
            raise ZeroDivisionError
        action(self.board, controller=self.controller, board_printer=self.boardPrinter)
        self.board.end_turn()
        return None

    def mulligan_all(self) -> None:
        for i in range(len(self.board.players)):
            self.print(i)
            self._mulligan_player(i)
        return None

    def print(self, select_index: int = None) -> None:
        self.boardPrinter.print(select_index)
        return None

    def _mulligan_player(self, player_index: int) -> None:
        player = self.board.players[player_index]
        wants_to_mulligan = self.controller.get_response([self.prompt_manager["mulligan_yn"]],
                                                         [rc.IsYesOrNo()])[0] == "y"

        while wants_to_mulligan:
            swap = self.controller.get_response(
                [self.prompt_manager["mulligan_hand_index"], self.prompt_manager["mulligan_fuk_index"]],
                [rc.IsWithinRange(0, 3), rc.IsWithinRange(0, 2)])
            player.swap_hand_card_with_karma(swap[0], swap[1])
            self.print(player_index)
            wants_to_mulligan = self.controller.get_response([self.prompt_manager["mulligan_yn"]],
                                                             [rc.IsYesOrNo()])[0] == "y"
        return None

    def choose_start_direction(self) -> None:
        self.print(self.board.player_index)
        direction = self.controller.get_response([self.prompt_manager["choose_direction"]],
                                                 [rc.IsInSet({"l", "r"})])
        if isinstance(direction[0], BoardTurnOrder):
            return self.board.set_turn_order(direction[0])
        elif direction[0].lower() == "r":
            return self.board.set_turn_order(BoardTurnOrder.RIGHT)
        self.board.set_turn_order(BoardTurnOrder.LEFT)
        return None

    @property
    def number_of_potential_winners(self) -> int:
        return sum(1 if len(player) == 0 else 0 for player in self.board.players)

    def __get_action_name(self, actions):
        action_names = [action.name() for action in actions]
        if len(actions) == 1:
            action_name = action_names[0]
        else:
            get_action_prompt = self.prompt_manager["select_action"]
            get_action_prompt.set_text(get_action_prompt.text + f" ({"/".join(action_names)})")
            action_name = self.controller.get_response([get_action_prompt],
                                                       [rc.IsInSet(set(action_names))])[0]
        return action_name

    def __card_selection_getter(self) -> Cards:
        lower_bound = 0
        upper_bound = len(self.board.current_player.playable_cards) - 1
        max_selection = len(self.board.current_player.playable_cards)
        get_card_indices_prompt = self.prompt_manager["select_cards_to_play"]
        get_card_indices_prompt.set_text(
            get_card_indices_prompt.text + f" From[{lower_bound}, {upper_bound}] - Pick up to {max_selection}")
        card_indices_selected = self.controller.get_response([get_card_indices_prompt],
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

        if number_of_potential_winners >= 2 and board.number_of_jokers_in_play == 0:
            raise GameWonException(self.game_ranks)
        if number_of_potential_winners >= 2:
            self.__vote_for_winners(board)
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

    def __vote_for_winners(self, board: IBoard) -> None:
        votes = defaultdict(int)
        joker_counts = {}
        for player_index, player in enumerate(board.players):
            joker_count = board.players[player_index].number_of_jokers
            if joker_count > 0:
                joker_counts[player_index] = joker_count
        player_indices = {x for x in range(len(board.players))}
        player_indices_to_exclude_from_vote = player_indices - board.potential_winner_indices
        for player_index, number_of_votes in joker_counts.items():
            board.set_player_index(player_index)
            vote_player_prompt = self.prompt_manager["vote_for_winner"]
            vote_player_prompt.set_text("Hi player: {player_index}. " + vote_player_prompt.text)
            player_vote = self.controller.get_response([vote_player_prompt],
                                                       [rc.IsNumberSelection(0, len(board.players),
                                                                             max_selection_count=1,
                                                                             exclude=player_indices_to_exclude_from_vote)])
            votes[player_vote[0]] += number_of_votes

        if votes:
            most_votes = max(votes.values())
            player_indices_with_most_votes = {player_index for player_index, count in votes.items() if count == most_votes}
            loser_indices = player_indices - player_indices_with_most_votes
            for player_index in loser_indices:
                self.game_ranks[player_index] += 1
        return None


def main():
    print("No longer the main, try running \'example_code.py\' instead!")


if __name__ == "__main__":
    main()
