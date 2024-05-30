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
    def __init__(self, lower: int, upper: int, max_selection_count: int, min_selection_count: int=1, exclude: int | None | set[int]=None):
        self.lower = lower
        self.upper = upper
        self.min_selection_count = min_selection_count
        self.max_selection_count = max_selection_count
        self.exclude = exclude

    def __call__(self, response: list[int]) -> bool:
        valid_selection_count = self.min_selection_count <= len(response) <= self.max_selection_count

        exclude_check = self.__equals
        if isinstance(self.exclude, set):
            exclude_check = self.__in_set

        if self.exclude is not None:
            return all(self.lower <= x <= self.upper and not exclude_check(x, self.exclude) for x in response) and valid_selection_count
        return all(self.lower <= x <= self.upper for x in response) and valid_selection_count

    def output_type(self) -> TypeCaster | None:
        return lambda x: [int(x) for x in re_findall(r"[\w']+", x)]

    @staticmethod
    def __in_set(x: int, y: set[int]) -> bool:
        return x in y

    @staticmethod
    def __equals(x: int, y: int) -> bool:
        return x == y
