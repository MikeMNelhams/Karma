from collections import defaultdict

from src.utils.multiset import FrozenMultiset
from src.cards import Cards, CardValue


def equal_subsequence_permutations(seq: Cards) -> set[list[CardValue]]:
    if len(seq) == 0:
        return set()
    if len(seq) == 1:
        return set(FrozenMultiset([seq[0].value]))

    count = defaultdict(int)

    outputs = set()
    for card in seq:
        key = card.value
        count[key] += 1
        outputs.add(FrozenMultiset([key for _ in range(count[key])]))
    return outputs


def equal_subsequence_permutations_with_filler(seq: Cards,
                                               filler: CardValue,
                                               minimum_to_filler: int=2) -> set[list[CardValue]]:
    if len(seq) == 0:
        return set()
    if len(seq) == 1:
        return set(FrozenMultiset([seq[0].value]))

    count = defaultdict(int)
    outputs = set()
    for card in seq:
        key = card.value
        count[key] += 1
        outputs.add(FrozenMultiset([key for _ in range(count[key])]))

    filler_count = count[filler]
    if filler_count == 0:
        return outputs
    outputs_that_include_filler = set()
    for output in outputs:
        if len(output) < minimum_to_filler:
            continue
        for i in range(1, filler_count+1):
            outputs_that_include_filler.add(FrozenMultiset(list(output) + [filler for _ in range(i)]))

    return outputs | outputs_that_include_filler


def equal_subsequence_permutations_with_filler_and_filter(seq: Cards,
                                                          filler: CardValue,
                                                          _filter: callable,
                                                          minimum_to_filler: int=2) -> set[frozenset[CardValue]]:
    if len(seq) == 0:
        return set()
    if len(seq) == 1:
        if _filter(seq[0]):
            return set()
        return set(FrozenMultiset([seq[0].value]))

    count = defaultdict(int)
    outputs = set()
    for card in seq:
        key = card.value
        count[key] += 1
        if _filter(card):
            continue
        outputs.add(FrozenMultiset([key for _ in range(count[key])]))

    filler_count = count[filler]
    if filler_count == 0:
        return outputs
    outputs_that_include_filler = set()
    for output in outputs:
        if len(output) < minimum_to_filler:
            continue
        for i in range(1, filler_count+1):
            outputs_that_include_filler.add(FrozenMultiset(list(output) + [filler for _ in range(i)]))

    return outputs | outputs_that_include_filler
