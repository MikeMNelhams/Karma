from typing import Any, Callable

import time

from response_conditions import ResponseCondition

from controller_interface import IController
from prompt_manager import Prompt
from bot_interface import IBot, BotNotReadyError


class PlayerController(IController):
    def __init__(self):
        pass

    def get_response(self, prompts: list[Prompt], output_checks: list[ResponseCondition]) -> list[Any]:
        assert len(prompts) == len(output_checks), ValueError("The prompts must have a condition for each!")

        output_type_casters = [check.output_type() for check in output_checks]
        responses = []
        for prompt, output_check, cast_to_type in zip(prompts, output_checks, output_type_casters):
            answered_correctly = False
            current_response = ""
            while not answered_correctly:
                current_response = input(f"{prompt.text} ")
                if current_response.lower() == "quit":
                    raise InterruptedError("Exiting program")
                try:
                    current_response = cast_to_type(current_response)
                    answered_correctly = output_check(current_response)
                except ValueError as e:
                    current_response = -1
                    answered_correctly = False
            responses.append(current_response)
        if isinstance(responses[0], list) and len(responses[0]) == 1 and prompts[0].key != "select_cards_to_play":
            responses = responses[0]
        return responses


class BotController(IController):
    def __init__(self, bot: IBot):
        self.__bot = bot
        self.__response_from_prompt_map = {"give_away": bot.card_giveaway_index,
                                           "give_away_select_player": bot.card_giveaway_player_index,
                                           "joker_select_player": bot.joker_target_index,
                                           "mulligan_yn": bot.wants_to_mulligan,
                                           "mulligan_hand_index": bot.mulligan_hand_index,
                                           "mulligan_fuk_index": bot.mulligan_fuk_index,
                                           "choose_direction": bot.preferred_start_direction,
                                           "select_action": bot.action,
                                           "select_cards_to_play": bot.card_play_indices,
                                           "vote_for_winner": bot.vote_for_winner_index}

    def get_response(self, prompts: list[str], output_checks: list[ResponseCondition]) -> list[Any]:
        assert len(prompts) == len(output_checks), ValueError("The prompts must have a condition for each!")
        time.sleep(self.__bot.delay)  # Otherwise the bot might end before you can even read what's happening!!!
        output_type_casters = [check.output_type() for check in output_checks]
        responses = []
        for prompt, output_check, cast_to_type in zip(prompts, output_checks, output_type_casters):
            assert self.bot.is_ready, BotNotReadyError(self.bot)

            response = self._response_from_prompt(prompt)
            responses.append(response)
        return responses

    @property
    def bot(self) -> IBot:
        return self.__bot

    def _response_from_prompt(self, prompt: Prompt) -> Any:
        response_getter: Callable[[], Any] = self.__response_from_prompt_map[prompt.key]
        return response_getter()
