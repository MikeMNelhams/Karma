from typing import Any

from response_conditions import ResponseCondition


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def ask_user(prompts: list[str], output_checks: list[ResponseCondition]) -> list[Any]:
        assert len(prompts) == len(output_checks), ValueError("The prompts must have a condition for each!")

        output_type_casters = [check.output_type() for check in output_checks]
        responses = []
        for prompt, output_check, cast_to_type in zip(prompts, output_checks, output_type_casters):
            answered_correctly = False
            current_response = ""
            while not answered_correctly:
                current_response = input(f"{prompt} ")
                if current_response.lower() == "quit":
                    raise InterruptedError("Exiting program")
                try:
                    current_response = cast_to_type(current_response)
                    answered_correctly = output_check(current_response)
                except ValueError as e:
                    current_response = -1
                    answered_correctly = False
            responses.append(current_response)
        return responses
