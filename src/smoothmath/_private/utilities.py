from __future__ import annotations
from typing import TypeVar, Any, Callable, Optional


U = TypeVar("U")
V = TypeVar("V")
W = TypeVar("W")


### Object utility functions ###


def get_class_name(
    any: Any
) -> str:
    return any.__class__.__name__


### Number utility functions ###


# This is_integer() function will be no longer needed as of Python 3.12
# when the is_integer() method is defined on int objects.


def is_integer(
    number: int | float
) -> bool:
    return isinstance(number, int) or (isinstance(number, float) and number.is_integer())


def integer_from_integral_float(
    number: int | float
) -> Optional[int]:
    if is_integer(number):
        return round(number)
    else:
        return None


def is_even(
    number: int
) -> bool:
    return number % 2 == 0


def is_odd(
    number: int
) -> bool:
    return number % 2 == 1


### List utility functions ###


def list_without_entry_at(
    entries: list[U],
    i: int
) -> list[U]:
    length = len(entries)
    if i >= length or i <= -(length + 1):
        return entries[:]
    if i >= 0:
        j = i
    else: # -length <= i <= -1
        j = length + i
    return entries[0:j] + entries[j + 1:]


def list_with_updated_entry_at(
    entries: list[U],
    i: int,
    new_entry: U
) -> list[U]:
    length = len(entries)
    if i >= length or i <= -(length + 1):
        return entries[:]
    if i >= 0:
        j = i
    else: # -length <= i <= -1
        j = length + i
    return entries[0:j] + [new_entry] + entries[j + 1:]


def first_match_by_predicate(
    entries: list[U],
    predicate: Callable[[U], bool]
) -> Optional[tuple[int, U]]:
    for i, entry in enumerate(entries):
        if predicate(entry):
            return (i, entry)
    return None


def partition_by_predicate(
    entries: list[U],
    predicate: Callable[[U], bool]
) -> tuple[list[U], list[U]]:
    hits = []
    misses = []
    for item in entries:
        if predicate(item):
            hits.append(item)
        else:
            misses.append(item)
    return hits, misses


### Dictionary utility functions ###


def group_by_key(
    values: list[V],
    key_from_value: Callable[[V], U]
) -> dict[U, list[V]]:
    values_by_key = dict()
    for value in values:
        key = key_from_value(value)
        if key not in values_by_key:
            values_by_key[key] = []
        values_by_key[key].append(value)
    return values_by_key


def map_dictionary_values(
    dictionary: dict[U, V],
    update_value: Callable[[U, V], W]
) -> dict[U, W]:
    result = dict()
    for key, value in dictionary.items():
        result[key] = update_value(key, value)
    return result
