from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression
    from smoothmath.expression import Variable


class GlobalPartial:
    """
    The partial derivative of an expression.

    :param expression: an expression
    :param variable: the partial is taken with respect to this variable
    """

    def __init__(
        self: GlobalPartial,
        expression: Expression,
        variable: Variable | str,
        synthetic_partial: Optional[Expression] = None
    ) -> None:
        variable_name = util.get_variable_name(variable)
        self._original_expression: Expression
        self._original_expression = expression
        self._variable_name: str
        self._variable_name = variable_name
        self._synthetic_partial: Expression
        self._synthetic_partial = _retrieve_synthetic_partial(
            expression,
            variable_name,
            synthetic_partial
        )

    def at(
        self: GlobalPartial,
        point: Point
    ) -> RealNumber:
        """
        Localize the partial derivative at a point.

        :param point: where to localize
        """
        # We evaluate the original expression to check for DomainErrors.
        # e.g. (ln(x))' = 1 / x
        # Notice that the RHS appears defined for negative x, but ln(x) isn't defined there!
        self._original_expression.evaluate(point)
        return self._synthetic_partial.evaluate(point)

    def __eq__(
        self: GlobalPartial,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (self._original_expression == other._original_expression) and
            (self._synthetic_partial == other._synthetic_partial)
        )

    def __hash__(
        self: GlobalPartial
    ) -> int:
        return hash((self._original_expression, self._synthetic_partial))

    def __str__(
        self: GlobalPartial
    ) -> str:
        return self._to_string()

    def __repr__(
        self: GlobalPartial
    ) -> str:
        return self._to_string()

    def _to_string(
        self: GlobalPartial
    ) -> str:
        variable_string = f"Variable(\"{self._variable_name}\")"
        return f"GlobalPartial({self._original_expression}, {variable_string})"


def _retrieve_synthetic_partial(
    original_expression: Expression,
    variable_name: str,
    optional_synthetic_partial: Optional[Expression]
) -> Expression:
    if optional_synthetic_partial is not None:
        return optional_synthetic_partial
    return original_expression._synthetic_partial(variable_name)._normalize()
