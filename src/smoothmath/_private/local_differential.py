from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression
    from smoothmath.expression import Variable


class LocalDifferential:
    """
    The differential of an expression localized at a point.

    :param expression: an expression
    :param point: where to localize
    """

    def __init__(
        self: LocalDifferential,
        expression: Expression,
        point: Point,
        numeric_partials: Optional[dict[str, RealNumber]] = None
    ) -> None:
        self._original_expression: Expression
        self._original_expression = expression
        self._point: Point
        self._point = point
        self._numeric_partials: dict[str, RealNumber]
        self._numeric_partials = _retrieve_numeric_partials(expression, point, numeric_partials)

    def component(
        self: LocalDifferential,
        variable: Variable | str
    ) -> RealNumber:
        """
        The component of the differential.

        :param variable: selects which component
        """
        variable_name = util.get_variable_name(variable)
        return self._numeric_partials.get(variable_name, 0)

    def __eq__(
        self: LocalDifferential,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (self._original_expression == other._original_expression) and
            (self._point == other._point) and
            (self._numeric_partials == other._numeric_partials)
        )

    def __hash__(
        self: LocalDifferential
    ) -> int:
        data = tuple(sorted(self._numeric_partials.items()))
        return hash((self._original_expression, self._point, data))

    def __str__(
        self: LocalDifferential
    ) -> str:
        return self._to_string()

    def __repr__(
        self: LocalDifferential
    ) -> str:
        return self._to_string()

    def _to_string(
        self: LocalDifferential
    ) -> str:
        return f"LocalDifferential({self._original_expression}, {self._point})"


def _retrieve_numeric_partials(
    original_expression: Expression,
    point: Point,
    optional_numeric_partials: Optional[dict[str, RealNumber]]
) -> dict[str, RealNumber]:
    if optional_numeric_partials is not None:
        return optional_numeric_partials
    else:
        return original_expression._numeric_partials(point)
