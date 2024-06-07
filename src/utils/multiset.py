# -*- coding: utf-8 -*-
"""An implementation of a multiset."""

from collections import defaultdict
from collections.abc import Iterable, Mapping, MutableMapping, Set, Sized, Container
from itertools import chain, repeat, starmap

_sequence_types = (tuple, list, range, set, frozenset, str)
_iter_types = (type(iter([])), type((lambda: (yield))()))

_all_basic_types = _sequence_types + _iter_types + (dict,)

__all__ = ['BaseMultiset', 'Multiset', 'FrozenMultiset']


# NOT MINE: https://pypi.org/project/multiset/

class BaseMultiset(object):
    """A multiset implementation by: https://pypi.org/project/multiset/
    :see: https://en.wikipedia.org/wiki/Multiset
    """

    __slots__ = ('_elements', '_total')

    def __init__(self, iterable=None):
        if isinstance(iterable, BaseMultiset):
            self._elements = iterable._elements.copy()
            self._total = iterable._total
        else:
            self._elements = _elements = defaultdict(int)
            _total = 0
            if iterable is not None:
                if isinstance(iterable, _sequence_types):
                    for element in iterable:
                        _elements[element] += 1
                    _total = len(iterable)
                elif isinstance(iterable, dict):
                    for element, multiplicity in iterable.items():
                        if multiplicity > 0:
                            _elements[element] = multiplicity
                            _total += multiplicity
                elif isinstance(iterable, _iter_types):
                    for element in iterable:
                        _elements[element] += 1
                        _total += 1
                elif isinstance(iterable, Mapping):
                    for element, multiplicity in iterable.items():
                        if multiplicity > 0:
                            _elements[element] = multiplicity
                            _total += multiplicity
                elif isinstance(iterable, Sized):
                    for element in iterable:
                        _elements[element] += 1
                    _total = len(iterable)
                else:
                    for element in iterable:
                        _elements[element] += 1
                        _total += 1
            self._total = _total

    def __new__(cls, iterable=None):
        if cls is BaseMultiset:
            raise TypeError("Cannot instantiate BaseMultiset directly, use either Multiset or FrozenMultiset.")
        return super(BaseMultiset, cls).__new__(cls)

    def __contains__(self, element):
        return element in self._elements

    def __getitem__(self, element):
        """The multiplicity of an element or zero if it is not in the multiset."""
        return self._elements.get(element, 0)

    def __str__(self):
        return '{%s}' % ', '.join(map(str, self.__iter__()))

    def __repr__(self):
        items = ', '.join('%r: %r' % item for item in self._elements.items())
        return '%s({%s})' % (self.__class__.__name__, items)

    def __len__(self):
        return self._total

    def __bool__(self):
        return self._total > 0

    def __iter__(self):
        return chain.from_iterable(starmap(repeat, self._elements.items()))

    def isdisjoint(self, other):
        if isinstance(other, _sequence_types + (BaseMultiset,)):
            pass
        elif not isinstance(other, Container):
            other = self._as_multiset(other)
        return all(element not in other for element in self._elements.keys())

    def difference(self, *others):
        result = self.__copy__()
        _elements = result._elements
        _total = result._total
        for other in map(self._as_multiset, others):
            for element, multiplicity in other.items():
                if element in _elements:
                    old_multiplicity = _elements[element]
                    new_multiplicity = old_multiplicity - multiplicity
                    if new_multiplicity > 0:
                        _elements[element] = new_multiplicity
                        _total -= multiplicity
                    else:
                        del _elements[element]
                        _total -= old_multiplicity
        result._total = _total
        return result

    def __sub__(self, other):
        if isinstance(other, (BaseMultiset, set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        return self.difference(other)

    def __rsub__(self, other):
        if not isinstance(other, (Set, BaseMultiset)):
            return NotImplemented
        return self._as_multiset(other).difference(self)

    def union(self, *others):
        result = self.__copy__()
        _elements = result._elements
        _total = result._total
        for other in map(self._as_mapping, others):
            for element, multiplicity in other.items():
                old_multiplicity = _elements.get(element, 0)
                if multiplicity > old_multiplicity:
                    _elements[element] = multiplicity
                    _total += multiplicity - old_multiplicity
        result._total = _total
        return result

    def __or__(self, other):
        if isinstance(other, (BaseMultiset, set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        return self.union(other)

    __ror__ = __or__

    def combine(self, *others):
        result = self.__copy__()
        _elements = result._elements
        _total = result._total
        for other in map(self._as_mapping, others):
            for element, multiplicity in other.items():
                old_multiplicity = _elements.get(element, 0)
                new_multiplicity = old_multiplicity + multiplicity
                if old_multiplicity > 0 >= new_multiplicity:
                    del _elements[element]
                    _total -= old_multiplicity
                elif new_multiplicity > 0:
                    _elements[element] = new_multiplicity
                    _total += multiplicity
        result._total = _total
        return result

    def __add__(self, other):
        if isinstance(other, (BaseMultiset, set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        return self.combine(other)

    __radd__ = __add__

    def intersection(self, *others):
        result = self.__copy__()
        _elements = result._elements
        _total = result._total
        for other in map(self._as_mapping, others):
            for element, multiplicity in list(_elements.items()):
                new_multiplicity = other.get(element, 0)
                if new_multiplicity < multiplicity:
                    if new_multiplicity > 0:
                        _elements[element] = new_multiplicity
                        _total -= multiplicity - new_multiplicity
                    else:
                        del _elements[element]
                        _total -= multiplicity
        result._total = _total
        return result

    def __and__(self, other):
        if isinstance(other, (BaseMultiset, set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        return self.intersection(other)

    __rand__ = __and__

    def symmetric_difference(self, other):
        other = self._as_multiset(other)
        result = self.__class__()
        _total = 0
        _elements = result._elements
        self_elements = self._elements
        other_elements = other._elements
        dist_elements = set(self_elements.keys()) | set(other_elements.keys())
        for element in dist_elements:
            multiplicity = self_elements.get(element, 0)
            other_multiplicity = other_elements.get(element, 0)
            new_multiplicity = (multiplicity - other_multiplicity
                                if multiplicity > other_multiplicity else other_multiplicity - multiplicity)
            _total += new_multiplicity
            if new_multiplicity > 0:
                _elements[element] = new_multiplicity
        result._total = _total
        return result

    def __xor__(self, other):
        if isinstance(other, (BaseMultiset, set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        return self.symmetric_difference(other)

    __rxor__ = __xor__

    def times(self, factor):
        if factor == 0:
            return self.__class__()
        if factor < 0:
            raise ValueError('The factor must no be negative.')
        result = self.__copy__()
        _elements = result._elements
        for element in _elements:
            _elements[element] *= factor
        result._total *= factor
        return result

    def __mul__(self, factor):
        if not isinstance(factor, int):
            return NotImplemented
        return self.times(factor)

    __rmul__ = __mul__

    def _issubset(self, other, strict):
        other = self._as_multiset(other)
        self_len = self._total
        other_len = len(other)
        if self_len > other_len:
            return False
        if self_len == other_len and strict:
            return False
        return all(multiplicity <= other[element] for element, multiplicity in self.items())

    def issubset(self, other):
        return self._issubset(other, False)

    def __le__(self, other):
        if isinstance(other, (BaseMultiset, set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        return self._issubset(other, False)

    def __lt__(self, other):
        if isinstance(other, (BaseMultiset, set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        return self._issubset(other, True)

    def _issuperset(self, other, strict):
        other = self._as_multiset(other)
        other_len = len(other)
        if len(self) < other_len:
            return False
        if len(self) == other_len and strict:
            return False
        for element, multiplicity in other.items():
            if self[element] < multiplicity:
                return False
        return True

    def issuperset(self, other):
        return self._issuperset(other, False)

    def __ge__(self, other):
        if isinstance(other, (BaseMultiset, set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        return self._issuperset(other, False)

    def __gt__(self, other):
        if isinstance(other, (BaseMultiset, set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        return self._issuperset(other, True)

    def __eq__(self, other):
        if isinstance(other, BaseMultiset):
            return self._total == other._total and self._elements == other._elements
        if isinstance(other, (set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        if self._total != len(other):
            return False
        return self._issubset(other, False)

    def __ne__(self, other):
        if isinstance(other, BaseMultiset):
            return self._total != other._total or self._elements != other._elements
        if isinstance(other, (set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        if self._total != len(other):
            return True
        return not self._issubset(other, False)

    def get(self, element, default):
        return self._elements.get(element, default)

    @classmethod
    def from_elements(cls, elements, multiplicity):
        return cls(dict.fromkeys(elements, multiplicity))

    def copy(self):
        """Return a shallow copy of the multiset."""
        return self.__class__(self)

    __copy__ = copy

    def items(self):
        return self._elements.items()

    def distinct_elements(self):
        return self._elements.keys()

    def multiplicities(self):
        return self._elements.values()

    values = multiplicities

    @classmethod
    def _as_multiset(cls, other):
        if isinstance(other, BaseMultiset):
            return other
        if isinstance(other, _all_basic_types):
            pass
        elif not isinstance(other, Iterable):
            raise TypeError("'%s' object is not iterable" % type(other))  # pragma: no cover
        return cls(other)

    @staticmethod
    def _as_mapping(iterable):
        if isinstance(iterable, BaseMultiset):
            return iterable._elements
        if isinstance(iterable, dict):
            return iterable
        if isinstance(iterable, _all_basic_types):
            pass  # create dictionary below
        elif isinstance(iterable, Mapping):
            return iterable
        elif not isinstance(iterable, Iterable):
            raise TypeError("'%s' object is not iterable" % type(iterable))
        mapping = dict()
        for element in iterable:
            if element in mapping:
                mapping[element] += 1
            else:
                mapping[element] = 1
        return mapping

    def __getstate__(self):
        return self._total, self._elements

    def __setstate__(self, state):
        self._total, self._elements = state


class Multiset(BaseMultiset):
    """The mutable multiset variant."""
    __slots__ = ()

    def __setitem__(self, element, multiplicity):
        if not isinstance(multiplicity, int):
            raise TypeError('multiplicity must be an integer')
        _elements = self._elements
        if element in _elements:
            old_multiplicity = _elements[element]
            if multiplicity > 0:
                _elements[element] = multiplicity
                self._total += multiplicity - old_multiplicity
            else:
                del _elements[element]
                self._total -= old_multiplicity
        elif multiplicity > 0:
            _elements[element] = multiplicity
            self._total += multiplicity

    def __delitem__(self, element):
        _elements = self._elements
        if element in _elements:
            self._total -= _elements[element]
            del _elements[element]
        else:
            raise KeyError("Could not delete {!r} from the multiset, because it is not in it.".format(element))

    def update(self, *others, **kwargs):
        _elements = self._elements
        _total = self._total
        for other in map(self._as_mapping, others + (kwargs,)):
            for element, multiplicity in other.items():
                if multiplicity > 0:
                    old_multiplicity = _elements.get(element, 0)
                    _elements[element] = multiplicity + old_multiplicity
                    _total += multiplicity
        self._total = _total

    def union_update(self, *others):

        _elements = self._elements
        _total = self._total
        for other in map(self._as_mapping, others):
            for element, multiplicity in other.items():
                old_multiplicity = _elements.get(element, 0)
                if multiplicity > old_multiplicity:
                    _elements[element] = multiplicity
                    _total += multiplicity - old_multiplicity
        self._total = _total

    def __ior__(self, other):
        if isinstance(other, (BaseMultiset, set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        self.union_update(other)
        return self

    def intersection_update(self, *others):
        for other in map(self._as_mapping, others):
            for element, current_count in list(self.items()):
                multiplicity = other.get(element, 0)
                if multiplicity < current_count:
                    self[element] = multiplicity

    def __iand__(self, other):
        if isinstance(other, (BaseMultiset, set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        self.intersection_update(other)
        return self

    def difference_update(self, *others):
        for other in map(self._as_multiset, others):
            for element, multiplicity in other.items():
                self.discard(element, multiplicity)

    def __isub__(self, other):
        if isinstance(other, (BaseMultiset, set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        self.difference_update(other)
        return self

    def symmetric_difference_update(self, other):
        other = self._as_multiset(other)
        elements = set(self.distinct_elements()) | set(other.distinct_elements())
        for element in elements:
            multiplicity = self[element]
            other_count = other[element]
            self[element] = (multiplicity - other_count if multiplicity > other_count else other_count - multiplicity)

    def __ixor__(self, other):
        if isinstance(other, (BaseMultiset, set, frozenset)):
            pass
        elif not isinstance(other, Set):
            return NotImplemented
        self.symmetric_difference_update(other)
        return self

    def times_update(self, factor):
        if factor < 0:
            raise ValueError("The factor must not be negative.")
        elif factor == 0:
            self.clear()
        else:
            _elements = self._elements
            for element in _elements:
                _elements[element] *= factor
            self._total *= factor

    def __imul__(self, factor):
        if not isinstance(factor, int):
            raise TypeError("factor must be an integer.")
        self.times_update(factor)
        return self

    def add(self, element, multiplicity=1):
        if multiplicity < 1:
            raise ValueError("Multiplicity must be positive")
        self._elements[element] += multiplicity
        self._total += multiplicity

    def remove(self, element, multiplicity=None):
        _elements = self._elements
        if element not in _elements:
            raise KeyError
        old_multiplicity = _elements.get(element, 0)
        if multiplicity is None or multiplicity >= old_multiplicity:
            del _elements[element]
            self._total -= old_multiplicity
        elif multiplicity < 0:
            raise ValueError("Multiplicity must be not be negative")
        elif multiplicity > 0:
            _elements[element] -= multiplicity
            self._total -= multiplicity
        return old_multiplicity

    def discard(self, element, multiplicity=None):
        _elements = self._elements
        if element in _elements:
            old_multiplicity = _elements[element]
            if multiplicity is None or multiplicity >= old_multiplicity:
                del _elements[element]
                self._total -= old_multiplicity
            elif multiplicity < 0:
                raise ValueError("Multiplicity must not be negative")
            elif multiplicity > 0:
                _elements[element] -= multiplicity
                self._total -= multiplicity
            return old_multiplicity
        else:
            return 0

    def pop(self, element, default):
        """If *element* is in the multiset, remove it and return its multiplicity, else return *default*.

        Makes the *default* argument of the original :meth:`dict.pop` non-optional.

        Args:
            element: The element which is removed.
            default: The default value to return if the element if not in the multiset.

        Returns:
            The multiplicity for *element* if it is in the multiset, else *default*.
        """
        rm_size = self._elements.get(element)
        if rm_size is not None:
            self._total -= rm_size
        return self._elements.pop(element, default)

    def setdefault(self, element, default):
        mul = self._elements.get(element)
        if mul is None:
            if default < 1:
                raise ValueError("Multiplicity must be positive")
            self._total += default
        return self._elements.setdefault(element, default)

    def clear(self):
        """Empty the multiset."""
        self._elements.clear()
        self._total = 0


class FrozenMultiset(BaseMultiset):
    """The frozen multiset variant that is immutable and hashable."""
    __slots__ = ()

    def __hash__(self):
        return hash(frozenset(self._elements.items()))


Mapping.register(BaseMultiset)  # type: ignore
MutableMapping.register(Multiset)  # type: ignore
