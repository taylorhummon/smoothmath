import math
from smoothmath.expression import Variable, Constant
from smoothmath._private.utilities import (
    get_class_name,
    is_integer,
    integer_from_integral_real_number,
    is_even,
    is_odd,
    list_without_entry_at,
    list_with_updated_entry_at,
    first_match_by_predicate,
    partition_by_predicate,
    group_by_key,
    map_dictionary_values,
    get_variable_name
)


def test_get_class_name():
    assert get_class_name(Variable("x")) == "Variable"
    assert get_class_name(Constant(3)) == "Constant"
    assert get_class_name(3) == "int"


def test_is_integer():
    assert is_integer(3) == True
    assert is_integer(3.0) == True
    assert is_integer(3.7) == False
    assert is_integer("3") == False # type: ignore
    assert is_integer(0.0) == True
    assert is_integer(-0.0) == True
    assert is_integer(math.inf) == False
    assert is_integer(-math.inf) == False
    assert is_integer(math.nan) == False


def test_integer_from_integral_real_number():
    assert integer_from_integral_real_number(3) == 3
    assert integer_from_integral_real_number(3.0) == 3
    assert integer_from_integral_real_number(3.7) == None
    assert integer_from_integral_real_number("3") == None # type: ignore
    assert integer_from_integral_real_number(0.0) == 0
    assert integer_from_integral_real_number(-0.0) == 0
    assert integer_from_integral_real_number(math.inf) == None
    assert integer_from_integral_real_number(-math.inf) == None
    assert integer_from_integral_real_number(math.nan) == None


def test_is_even():
    assert is_even(2) == True
    assert is_even(1) == False
    assert is_even(0) == True
    assert is_even(-1) == False
    assert is_even(-2) == True


def test_is_odd():
    assert is_odd(2) == False
    assert is_odd(1) == True
    assert is_odd(0) == False
    assert is_odd(-1) == True
    assert is_odd(-2) == False


def test_list_without_entry_at():
    entries = [0, 1, 2]
    list_without_entry_at([0, 1, 2], 1)
    assert entries == [0, 1, 2] # verify list_without_entry_at does not mutate entries
    entries = ["x", "y", "z"]
    copy = list_without_entry_at(entries, 50)
    assert copy == entries
    assert copy is not entries
    entries = []
    assert list_without_entry_at(entries, 0) == []
    assert list_without_entry_at(entries, -1) == []
    entries = ["orange"]
    assert list_without_entry_at(entries, 0) == []
    assert list_without_entry_at(entries, -1) == []
    assert list_without_entry_at(entries, 1) == ["orange"]
    assert list_without_entry_at(entries, -2) == ["orange"]
    entries = ["a", "b", "c", "a", "b", "c"]
    assert list_without_entry_at(entries, 0) == ["b", "c", "a", "b", "c"]
    assert list_without_entry_at(entries, 3) == ["a", "b", "c", "b", "c"]
    assert list_without_entry_at(entries, 5) == ["a", "b", "c", "a", "b"]
    assert list_without_entry_at(entries, 6) == ["a", "b", "c", "a", "b", "c"]
    assert list_without_entry_at(entries, -1) == ["a", "b", "c", "a", "b"]
    assert list_without_entry_at(entries, -6) == ["b", "c", "a", "b", "c"]
    assert list_without_entry_at(entries, -7) == ["a", "b", "c", "a", "b", "c"]


def test_list_with_updated_entry_at():
    entries = [0, 1, 2]
    list_with_updated_entry_at([0, 1, 2], 1, 7)
    assert entries == [0, 1, 2] # verify list_with_updated_entry_at does not mutate entries
    entries = ["x", "y", "z"]
    copy = list_with_updated_entry_at(entries, 50, "a")
    assert copy == entries
    assert copy is not entries
    entries = []
    assert list_with_updated_entry_at(entries, 0, 7) == []
    assert list_with_updated_entry_at(entries, -1, 7) == []
    entries = ["orange"]
    assert list_with_updated_entry_at(entries, 0, "red") == ["red"]
    assert list_with_updated_entry_at(entries, -1, "red") == ["red"]
    assert list_with_updated_entry_at(entries, 1, "red") == ["orange"]
    assert list_with_updated_entry_at(entries, -2, "red") == ["orange"]
    entries = ["a", "b", "c", "a", "b", "c"]
    assert list_with_updated_entry_at(entries, 0, "x") == ["x", "b", "c", "a", "b", "c"]
    assert list_with_updated_entry_at(entries, 3, "x") == ["a", "b", "c", "x", "b", "c"]
    assert list_with_updated_entry_at(entries, 5, "x") == ["a", "b", "c", "a", "b", "x"]
    assert list_with_updated_entry_at(entries, 6, "x") == ["a", "b", "c", "a", "b", "c"]
    assert list_with_updated_entry_at(entries, -1, "x") == ["a", "b", "c", "a", "b", "x"]
    assert list_with_updated_entry_at(entries, -6, "x") == ["x", "b", "c", "a", "b", "c"]
    assert list_with_updated_entry_at(entries, -7, "x") == ["a", "b", "c", "a", "b", "c"]


def test_index_of_first_match():
    entries = ["a", "b", "c", "a", "b", "c"]
    assert first_match_by_predicate(entries, lambda entry: entry == "a") == (0, "a")
    assert first_match_by_predicate(entries, lambda entry: entry == "c") == (2, "c")
    assert first_match_by_predicate(entries, lambda entry: entry == "d") == None
    entries = []
    assert first_match_by_predicate(entries, lambda entry: entry == 7) == None
    assert first_match_by_predicate(entries, lambda entry: entry == []) == None


def test_partition_by_predicate():
    entries = [1, 2, 3, 1, 2, 3]
    assert partition_by_predicate(entries, lambda entry: entry % 2 == 0) == ([2, 2], [1, 3, 1, 3])
    assert partition_by_predicate(entries, lambda _: True) == (entries, [])
    assert partition_by_predicate(entries, lambda _: False) == ([], entries)
    entries = []
    assert partition_by_predicate(entries, lambda _: True) == ([], [])


def test_group_by_key():
    values = [1, 2, 3, 1, 2, 3]
    assert group_by_key(values, lambda value: value % 2) == {0: [2, 2], 1: [1, 3, 1, 3]}
    values = []
    assert group_by_key(values, lambda value: value) == {}


def test_map_dictionary_values():
    dictionary = {"a": 1, "b": 2, "c": 3}
    assert map_dictionary_values(dictionary, lambda _, value: value + 5) == {"a": 6, "b": 7, "c": 8}
    assert map_dictionary_values(dictionary, lambda key, _: key.upper()) == {"a": "A", "b": "B", "c": "C"}
    dictionary = {}
    assert map_dictionary_values(dictionary, lambda _, value: value) == {}


def test_get_variable_name():
    assert get_variable_name(Variable("x")) == "x"
    assert get_variable_name("y") == "y"
