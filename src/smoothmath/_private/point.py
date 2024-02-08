from __future__ import annotations
from typing import Any, Mapping
import smoothmath as sm
import smoothmath.expression as ex
from smoothmath._private.utilities import get_variable_name


class Point:
    """Represents a point by associating a real number to each variable x, y, ..."""

    def __init__(
        self: Point,
        dictionary: Mapping[ex.Variable | str, sm.real_number]
    ) -> None:
        self._value_by_variable_name: Mapping[str, sm.real_number]
        self._value_by_variable_name = {}
        for variable_or_name, value in dictionary.items():
            variable_name = get_variable_name(variable_or_name)
            if variable_name in self._value_by_variable_name:
                raise Exception(f"Provided more than one value for variable: {variable_name}")
            self._value_by_variable_name[variable_name] = value

    def value_for(
        self: Point,
        variable_or_name: ex.Variable | str
    ) -> sm.real_number:
        """
        Returns the real number associated to the given variable

        :param variable_or_name: a variable or its name as a string
        """
        variable_name = get_variable_name(variable_or_name)
        value = self._value_by_variable_name.get(variable_name, None)
        if value is None:
            raise Exception(f"No value provided for variable: {variable_name}")
        return value

    def __eq__(
        self: Point,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (other._value_by_variable_name == self._value_by_variable_name)
        )

    def __hash__(
        self: Point
    ) -> int:
        data = tuple(sorted(self._value_by_variable_name.items()))
        return hash(data)

    def __str__(
        self: Point
    ) -> str:
        return self._to_string()

    def __repr__(
        self: Point
    ) -> str:
        return self._to_string()

    def _to_string(
        self: Point
    ) -> str:
        equations_string = ", ".join(
            f'"{variable_name}": {value}'
            for variable_name, value in self._value_by_variable_name.items()
        )
        return "Point({" + equations_string + "})"
