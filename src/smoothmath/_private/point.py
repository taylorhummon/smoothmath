from __future__ import annotations
from typing import TYPE_CHECKING, Any, Mapping
import smoothmath._private.expression.variable as va
import smoothmath._private.errors as er
if TYPE_CHECKING:
    from smoothmath.expression import Variable


class Point:
    """
    A point. Can have any number of coordinates.

    >>> from smoothmath import Point
    >>> Point(x=3, y=4.5)
    Point(x=3, y=4.5)

    :param \\*\\*kwargs: a real number for each coordinate name
    """

    def __init__(
        self: Point,
        **kwargs: float
    ) -> None:
        self._coordinates: Mapping[str, float]
        self._coordinates = kwargs

    def coordinate(
        self: Point,
        variable: Variable | str
    ) -> float:
        """
        Retrieves a coordinate.

        Raises :exc:`~smoothmath.CoordinateMissing` if the point has no entry for
        the coordinate name.

        >>> from smoothmath import Point
        >>> point = Point(x=3, y=4.5)
        >>> point.coordinate("x")
        3
        >>> point.coordinate("y")
        4.5

        :param variable: selects which coordinate
        """
        variable_name = va.get_variable_name(variable)
        value = self._coordinates.get(variable_name, None)
        if value is None:
            raise er.CoordinateMissing(f"Point has no coordinate for variable: {variable_name}")
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
        return hash(("Point", data))

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
            f'{variable_name}={value}'
            for variable_name, value in self._coordinates.items()
        )
        return f"Point({equations_string})"


def point_on_number_line(
    variable_name: str,
    value: float
) -> Point:
    return Point(**({variable_name: value}))
