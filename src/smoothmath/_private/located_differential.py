from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
import smoothmath._private.expression.variable as va
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression
    from smoothmath.expression import Variable


class LocatedDifferential:
    """
    The differential of an expression located at a point.

    :param expression: an expression
    :param point: where to locate the differential
    """

    def __init__(
        self: LocatedDifferential,
        expression: Expression,
        point: Point,
        numeric_partials: Optional[dict[str, RealNumber]] = None
    ) -> None:
        self._original_expression: Expression
        self._original_expression = expression
        self._point: Point
        self._point = point
        self._numeric_partials: dict[str, RealNumber]
        self._numeric_partials = _initial_numeric_partials(expression, point, numeric_partials)

    def part(
        self: LocatedDifferential,
        variable: Variable | str
    ) -> RealNumber:
        """
        Retrieves a part of the differential.

        NOTE: The parts of the differential are the partials of the original expression.

        :param variable: selects which part
        """
        variable_name = va.get_variable_name(variable)
        return self._numeric_partials.get(variable_name, 0)

    def __eq__(
        self: LocatedDifferential,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (self._original_expression == other._original_expression) and
            (self._point == other._point)
        )

    def __hash__(
        self: LocatedDifferential
    ) -> int:
        return hash(("LocatedDifferential", self._original_expression, self._point))

    def __str__(
        self: LocatedDifferential
    ) -> str:
        return self._to_string()

    def __repr__(
        self: LocatedDifferential
    ) -> str:
        return self._to_string()

    def _to_string(
        self: LocatedDifferential
    ) -> str:
        return f"LocatedDifferential({self._original_expression}, {self._point})"


def _initial_numeric_partials(
    original_expression: Expression,
    point: Point,
    optional_numeric_partials: Optional[dict[str, RealNumber]]
) -> dict[str, RealNumber]:
    if optional_numeric_partials is not None:
        return optional_numeric_partials
    else:
        return original_expression._numeric_partials(point)
