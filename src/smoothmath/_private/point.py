from __future__ import annotations
from typing import Mapping
import smoothmath as sm
import smoothmath.expression as ex
from smoothmath._private.utilities import get_variable_name


class Point:
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
        variable_name = get_variable_name(variable_or_name)
        value = self._value_by_variable_name.get(variable_name, None)
        if value is None:
            raise Exception(f"No value provided for variable: {variable_name}")
        return value

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
        inner = ", ".join(
            f"{variable_name} = {value}"
            for variable_name, value in self._value_by_variable_name.items()
        )
        return f"({inner})"
