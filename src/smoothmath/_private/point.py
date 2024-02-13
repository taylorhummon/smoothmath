from __future__ import annotations
from typing import TYPE_CHECKING, Any, Mapping
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import RealNumber
    from smoothmath.expression import Variable


class Point:
    """
    A point. When constructing a point each keyword parameter is a variable name, and each
    keyword argument is a real number. The order of keyword parameters is ignored.

    >>> from smoothmath import Point
    >>> Point(x=3, y=4.5) == Point(y=4.5, x=3)
    True

    :param \\*\\*kwargs: a real number for each variable name
    """

    def __init__(
        self: Point,
        **kwargs: RealNumber
    ) -> None:
        self._coordinates: Mapping[str, RealNumber]
        self._coordinates = kwargs

    def coordinate(
        self: Point,
        variable: Variable | str
    ) -> RealNumber:
        """
        A coordinate. Raises an ``Exception`` if the variable is not present in the point.

        >>> from smoothmath import Point
        >>> p = Point(x=3, y=4.5)
        >>> p.coordinate("x")
        3
        >>> p.coordinate("y")
        4.5

        :param variable: selects which coordinate
        """
        variable_name = util.get_variable_name(variable)
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
            f'{variable_name}={value}'
            for variable_name, value in self._coordinates.items()
        )
        return f"Point({equations_string})"
