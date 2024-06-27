from collections import defaultdict

from src.utils.multiset import FrozenMultiset
from src.cards import Cards, CardValue


def equal_subsequence_permutations(seq: Cards) -> set[FrozenMultiset]:
    if len(seq) == 0:
        return set()
    if len(seq) == 1:
        return __single_value_frozen_multiset(seq)

    count = defaultdict(int)

    outputs = set()
    for card in seq:
        key = card.value
        count[key] += 1
        outputs.add(FrozenMultiset([key for _ in range(count[key])]))
    return outputs


def equal_subsequence_permutations_filler(seq: Cards,
                                          filler: CardValue,
                                          minimum_to_filler: int = 2) -> set[FrozenMultiset]:
    if len(seq) == 0:
        return set()
    if len(seq) == 1:
        return __single_value_frozen_multiset(seq)

    count = defaultdict(int)
    outputs = set()
    for card in seq:
        key = card.value
        count[key] += 1
        outputs.add(FrozenMultiset([key for _ in range(count[key])]))

    filler_count = count[filler]
    outputs_that_include_filler = set()
    if filler_count == 0:
        return outputs
    for output in outputs:
        if len(output) < minimum_to_filler:
            continue
        for i in range(1, filler_count + 1):
            outputs_that_include_filler.add(FrozenMultiset(list(output) + [filler for _ in range(i)]))
    outputs |= outputs_that_include_filler
    outputs -= {FrozenMultiset([filler for _ in range(filler_count + i)]) for i in range(1, filler_count + 1)}
    return outputs | outputs_that_include_filler


def equal_subsequence_permutations_filler_not_exclusively_filler(seq: Cards,
                                                                 filler: CardValue,
                                                                 minimum_to_filler: int=2) -> set[FrozenMultiset]:
    if len(seq) == 0:
        return set()
    if len(seq) == 1:
        return __single_value_frozen_multiset(seq)

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
        for i in range(1, filler_count + 1):
            outputs_that_include_filler.add(FrozenMultiset(list(output) + [filler for _ in range(i)]))
    outputs |= outputs_that_include_filler
    outputs -= {FrozenMultiset([filler for _ in range(i)]) for i in range(1, filler_count * 2 + 1)}
    return outputs


def equal_subsequence_permutations_filler_and_filter(seq: Cards,
                                                     filler: CardValue,
                                                     _filter: callable,
                                                     minimum_to_filler: int = 2) -> set[FrozenMultiset]:
    if len(seq) == 0:
        return set()
    if len(seq) == 1:
        if _filter(seq[0]):
            return set()
        return __single_value_frozen_multiset(seq)

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
        for i in range(1, filler_count + 1):
            outputs_that_include_filler.add(FrozenMultiset(list(output) + [filler for _ in range(i)]))
    outputs |= outputs_that_include_filler
    outputs -= __not_exclusively_filler_but_contains_filler_frozen_multi_sets(filler, filler_count)
    return outputs


def equal_subsequence_permutations_filler_filter_not_exclusively_filler(seq: Cards,
                                                                        filler: CardValue,
                                                                        _filter: callable,
                                                                        minimum_to_filler: int = 2) -> set[FrozenMultiset]:
    if len(seq) == 0:
        return set()
    if len(seq) == 1:
        if _filter(seq[0]):
            return set()
        return __single_value_frozen_multiset(seq)

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
        for i in range(1, filler_count + 1):
            outputs_that_include_filler.add(FrozenMultiset(list(output) + [filler for _ in range(i)]))
    outputs |= outputs_that_include_filler
    outputs -= {FrozenMultiset([filler for _ in range(i)]) for i in range(1, filler_count * 2 + 1)}
    return outputs


def __single_value_frozen_multiset(seq):
    return {FrozenMultiset([seq[0].value])}


def __not_exclusively_filler_but_contains_filler_frozen_multi_sets(filler, filler_count):
    return {FrozenMultiset([filler for _ in range(filler_count + i)]) for i in range(1, filler_count + 1)}
