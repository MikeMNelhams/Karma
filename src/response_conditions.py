from abc import ABC, abstractmethod

from typing import Any, Callable

type TypeCaster = Callable[[str], Any]


class ResponseCondition(ABC):
    @abstractmethod
    def __call__(self, response: str) -> bool:
        raise NotImplementedError

    def output_type(self) -> TypeCaster | None:
        return lambda x: x


class IsYesOrNo(ResponseCondition):
    def __call__(self, response: str) -> bool:
        return response.lower() in ("y", "n")


class IsWithinRange(ResponseCondition):
    def __init__(self, lower: int, upper: int):
        self.lower = lower
        self.upper = upper

    def __call__(self, response: str) -> bool:
        return self.lower <= response <= self.upper

    def output_type(self) -> TypeCaster | None:
        return int
