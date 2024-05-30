from abc import ABC, abstractmethod

from typing import Any, Callable

from re import findall as re_findall

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


class IsInSet(ResponseCondition):
    def __init__(self, target: set[str]):
        self.target = target

    def __call__(self, response: str) -> bool:
        return response.lower() in self.target


class IsWithinRange(ResponseCondition):
    def __init__(self, lower: int, upper: int):
        self.lower = lower
        self.upper = upper

    def __call__(self, response: int) -> bool:
        return self.lower <= response <= self.upper

    def output_type(self) -> TypeCaster | None:
        return int


class IsNumberSelection(ResponseCondition):
    def __init__(self, lower: int, upper: int, max_selection_count: int):
        self.lower = lower
        self.upper = upper
        self.max_selection_count = max_selection_count

    def __call__(self, response: list[int]) -> bool:
        return all(self.lower <= x <= self.upper for x in response) and len(response) <= self.max_selection_count

    def output_type(self) -> TypeCaster | None:
        return lambda x: [int(x) for x in re_findall(r"[\w']+", x)]
