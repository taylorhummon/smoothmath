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
        self._synthetic_partial = _retrieve_normalized_synthetic_partial(
            expression, variable_name, synthetic_partial
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
        self._original_expression.evaluate(point)
        return self._synthetic_partial.evaluate(point)

    def as_expression(
        self: GlobalPartial
    ) -> Expression:
        """
        The global partial written as an expression.
        Sometimes referred to as the *synthetic partial*.

        NOTE: The synthetic partial may be defined at more points than the global partial.
        For example, take ``z = Logarithm(Variable("x"))`` and so the synthetic partial is
        ``Reciprocal(Variable("x"))``. The synthetic partial is defined for negative x values,
        but the global partial is only defined at positive x values.
        """
        return self._synthetic_partial

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


def _retrieve_normalized_synthetic_partial(
    original_expression: Expression,
    variable_name: str,
    optional_synthetic_partial: Optional[Expression]
) -> Expression:
    if optional_synthetic_partial is not None:
        # We'll assume that if a synthetic partial was passed in to the constructor,
        # we don't need to normalize it.
        return optional_synthetic_partial
    return original_expression._synthetic_partial(variable_name)._normalize()
