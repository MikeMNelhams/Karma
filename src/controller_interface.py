from abc import ABC, abstractmethod

from typing import Any

from response_conditions import ResponseCondition
from prompt_manager import Prompt


class IController(ABC):
    @abstractmethod
    def __init__(self, *args):
        raise NotImplementedError

    @abstractmethod
    def ask_user(self, prompts: list[Prompt], output_checks: list[ResponseCondition]) -> list[Any]:
        raise NotImplementedError
