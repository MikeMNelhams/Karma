from typing import Hashable, TypeVar

from collections import defaultdict

from src.cards import Cards


C = TypeVar('C')


def equal_subsequence_permutations(seq: Hashable) -> set:
    if len(seq) == 0:
        return set()
    if len(seq) == 1:
        return {seq}

    count = defaultdict(int)

    outputs = set()
    for x in seq:
        count[x] += 1
        outputs.add(Cards(x for _ in range(count[x])))
    return outputs


def equal_subsequence_permutations_with_filler(seq: Hashable, filler: int, minimum_to_filler: int=2) -> set:
    if len(seq) == 0:
        return set()
    if len(seq) == 1:
        return {seq}

    count = defaultdict(int)
    outputs = set()
    for x in seq:
        count[x] += 1
        outputs.add(Cards(x for _ in range(count[x])))

    filler_count = count[filler]
    if filler_count == 0:
        return outputs
    outputs_that_include_filler = set()
    for output in outputs:
        if len(output) < minimum_to_filler:
            continue
        for i in range(1, filler_count+1):
            outputs_that_include_filler.add(Cards(list(output) + [filler for _ in range(i)]))

    return outputs | outputs_that_include_filler


def equal_subsequence_permutations_with_filler_and_filter(seq: Hashable, filler: int, _filter: callable, minimum_to_filler: int=2) -> set:
    if len(seq) == 0:
        return set()
    if len(seq) == 1:
        return {seq}

    count = defaultdict(int)
    outputs = set()
    for x in seq:
        count[x] += 1
        if _filter(x):
            continue
        outputs.add(Cards(x for _ in range(count[x])))

    filler_count = count[filler]
    if filler_count == 0:
        return outputs
    outputs_that_include_filler = set()
    for output in outputs:
        if len(output) < minimum_to_filler:
            continue
        for i in range(1, filler_count+1):
            outputs_that_include_filler.add(Cards(list(output) + [filler for _ in range(i)]))

    return outputs | outputs_that_include_filler
