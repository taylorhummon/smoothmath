from __future__ import annotations
from typing import TYPE_CHECKING, Any, Mapping
import smoothmath.expression as ex
from smoothmath._private.utilities import get_variable_name
if TYPE_CHECKING:
    from smoothmath import RealNumber


class Point:
    def __init__(
        self: Point,
        coordinates: Mapping[ex.Variable | str, RealNumber]
    ) -> None:
        """
        A point.

        :param coordinates: A mapping associating a real number to each variable.
        """
        self._coordinates: Mapping[str, RealNumber]
        self._coordinates = {}
        for variable_or_name, value in coordinates.items():
            variable_name = get_variable_name(variable_or_name)
            if variable_name in self._coordinates:
                raise Exception(f"Provided more than one value for variable: {variable_name}")
            self._coordinates[variable_name] = value

    def coordinate(
        self: Point,
        variable: ex.Variable | str
    ) -> RealNumber:
        """
        A coordinate. The y coordinate of Point({"x": 3, y: "4"}) is 4.

        :param variable: a variable (or the variable's name)
        """
        variable_name = get_variable_name(variable)
        value = self._coordinates.get(variable_name, None)
        if value is None:
            raise Exception(f"No value provided for variable: {variable_name}")
        return value

    def __eq__(
        self: Point,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (other._coordinates == self._coordinates)
        )

    def __hash__(
        self: Point
    ) -> int:
        data = tuple(sorted(self._coordinates.items()))
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
            for variable_name, value in self._coordinates.items()
        )
        return "Point({" + equations_string + "})"
