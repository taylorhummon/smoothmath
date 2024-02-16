from __future__ import annotations
from typing import TYPE_CHECKING, Any
import smoothmath._private.partial as pa
import smoothmath._private.point as pt
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression, Partial


class Derivative:
    """
    The derivative of an expression.

    The expression must have only one variable. For alternatives without this limitation,
    see the Partial, Differential, and LocatedDifferential classes.

    Consider setting the ``compute_eagerly`` parameter to ``True`` as an optimization if the
    partial will be evaluated at many points.

    :param expression: an expression of one variable
    :param compute_eagerly: whether to do extra work on initialization to have faster ``at()`` evaluation after
    """

    def __init__(
        self: Derivative,
        expression: Expression,
        compute_eagerly: bool = False
    ) -> None:
        exception_message = "Can only take the derivative of an expression with one variable. Consider a Partial, Differential, or LocatedDifferential instead."
        variable_name = _get_the_single_variable_name(expression, exception_message)
        self._original_expression: Expression
        self._original_expression = expression
        self._variable_name: str
        self._variable_name = variable_name
        self._partial: Partial
        self._partial = pa.Partial(expression, variable_name, compute_eagerly = compute_eagerly)

    def at(
        self: Derivative,
        point: Point | RealNumber
    ) -> RealNumber:
        """
        Evaluate the derivative.

        :param point: where to evaluate the partial
        """
        if not isinstance(point, pt.Point):
            point = _point_on_number_line(self._variable_name, point)
        return self._partial.at(point)

    def as_expression(
        self: Derivative
    ) -> Expression:
        """
        The derivative written as an expression.
        Sometimes referred to as the *synthetic derivative*.

        NOTE: Writing the derivative as an expression may enlargen the domain.
        For example, take ``z = Logarithm(Variable("x"))`` and so the derivative as an expression is
        ``Reciprocal(Variable("x"))``. This expression representing the derivative is defined for
        negative x values, but the honest derivative is only defined at positive x values.
        """
        return self._partial.as_expression()

    def __eq__(
        self: Derivative,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (self._original_expression == other._original_expression)
        )

    def __hash__(
        self: Derivative
    ) -> int:
        return hash(self._original_expression)

    def __str__(
        self: Derivative
    ) -> str:
        return self._to_string()

    def __repr__(
        self: Derivative
    ) -> str:
        return self._to_string()

    def _to_string(
        self: Derivative
    ) -> str:
        return f"Derivative({self._original_expression})"


def _get_the_single_variable_name( # !!! DRY?
    expression: Expression,
    exception_message: str
) -> str:
    variable_names = expression._variable_names
    variable_names_count = len(variable_names)
    if variable_names_count == 1:
        (variable_name,) = variable_names
        return variable_name
    elif variable_names_count == 0:
        return "whatever"
    else:
        raise Exception(exception_message)


def _point_on_number_line( # !!! DRY?
    variable_name: str,
    value: RealNumber
) -> Point:
    return pt.Point(**({variable_name: value}))