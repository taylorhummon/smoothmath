from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
import smoothmath._private.expression.variable as va
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression
    from smoothmath.expression import Variable


class Partial:
    """
    The partial derivative of an expression.

    :param expression: an expression
    :param variable: the partial is taken with respect to this variable
    :param compute_eagerly: whether to do extra work on initialization to have faster evaluation afterwards
    """

    def __init__(
        self: Partial,
        expression: Expression,
        variable: Variable | str,
        compute_eagerly: bool = False,
        synthetic_partial: Optional[Expression] = None
    ) -> None:
        variable_name = va.get_variable_name(variable)
        self._original_expression: Expression
        self._original_expression = expression
        self._variable_name: str
        self._variable_name = variable_name
        self._synthetic_partial: Optional[Expression]
        self._synthetic_partial = _initial_synthetic_partial(
            expression, variable_name, compute_eagerly, synthetic_partial
        )

    def at(
        self: Partial,
        point: Point
    ) -> RealNumber:
        """
        Evaluate the partial at a point.

        :param point: where to evaluate the partial
        """
        if self._synthetic_partial is None:
            self._original_expression._reset_evaluation_cache()
            return self._original_expression._numeric_partial(self._variable_name, point)
        else:
            # We evaluate the original expression to check for DomainErrors.
            self._original_expression.at(point)
            return self._synthetic_partial.at(point)

    def as_expression(
        self: Partial
    ) -> Expression:
        """
        The partial written as an expression.
        Sometimes referred to as the *synthetic partial*.

        NOTE: Writing the partial as an expression may enlargen the domain.
        For example, take ``z = Logarithm(Variable("x"))`` and so the partial as an expression is
        ``Reciprocal(Variable("x"))``. This expression representing the partial is defined for
        negative x values, but the honest partial is only defined at positive x values.
        """
        if self._synthetic_partial is None:
            self._synthetic_partial = _retrieve_synthetic_partial(
                self._original_expression,
                self._variable_name
            )
        return self._synthetic_partial

    def __eq__(
        self: Partial,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (self._original_expression == other._original_expression) and
            (self._variable_name == other._variable_name)
        )

    def __hash__(
        self: Partial
    ) -> int:
        return hash(("Partial", self._original_expression))

    def __str__(
        self: Partial
    ) -> str:
        return self._to_string()

    def __repr__(
        self: Partial
    ) -> str:
        return self._to_string()

    def _to_string(
        self: Partial
    ) -> str:
        variable_string = f"Variable(\"{self._variable_name}\")"
        return f"Partial({self._original_expression}, {variable_string})"


def _initial_synthetic_partial(
    original_expression: Expression,
    variable_name: str,
    compute_eagerly: bool,
    optional_synthetic_partial: Optional[Expression]
) -> Optional[Expression]:
    if optional_synthetic_partial is not None:
        # We'll assume that if a synthetic partial was passed in to the constructor,
        # we don't need to normalize it.
        return optional_synthetic_partial
    elif compute_eagerly:
        return _retrieve_synthetic_partial(original_expression, variable_name)
    else:
        return None


def _retrieve_synthetic_partial(
    original_expression: Expression,
    variable_name: str
) -> Expression:
    return original_expression._synthetic_partial(variable_name)._normalize()
