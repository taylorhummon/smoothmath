from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
import smoothmath._private.expression.variable as va
if TYPE_CHECKING:
    from smoothmath import Point, Expression
    from smoothmath.expression import Variable


class LocatedDifferential:
    """
    The differential of an expression located at a point.

    >>> from smoothmath import Point, LocatedDifferential
    >>> from smoothmath.expression import Variable, Multiply
    >>> LocatedDifferential(Multiply(Variable("x"), Variable("y")), Point(x=2, y=4))
    LocatedDifferential(Multiply(Variable("x"), Variable("y")), Point(x=2, y=4))

    :param expression: an expression
    :param point: where to locate the differential
    """

    def __init__(
        self: LocatedDifferential,
        expression: Expression,
        point: Point,
        _private: Optional[dict[str, dict[str, float]]] = None
    ) -> None:
        self._original_expression: Expression
        self._original_expression = expression
        self._point: Point
        self._point = point
        self._numeric_partials: dict[str, float]
        self._numeric_partials = _initial_numeric_partials(expression, point, _private)

    def component(
        self: LocatedDifferential,
        variable: Variable | str
    ) -> float:
        """
        Retrieves a component of the differential.

        NOTE: The components of the differential are the partials of the original expression.

        :param variable: selects which component
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
    _private: Optional[dict[str, dict[str, float]]]
) -> dict[str, float]:
    if _private is not None and 'numeric_partials' in _private:
        return _private['numeric_partials']
    else:
        return original_expression._numeric_partials(point)
