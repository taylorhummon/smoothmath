from __future__ import annotations
from typing import TYPE_CHECKING, Any
import smoothmath._private.partial as pa
import smoothmath._private.point as pt
import smoothmath._private.base_expression.expression as be
if TYPE_CHECKING:
    from smoothmath import Point, Expression, Partial


class Derivative:
    """
    The derivative of an expression.

    >>> from smoothmath import Derivative
    >>> from smoothmath.expression import Variable, NthPower
    >>> Derivative(NthPower(Variable("x"), n=2))
    Derivative(NthPower(Variable("x"), n=2))

    NOTE: The expression must have only one variable. For alternatives that support
    expressions with multiple variables, see the :class:`Differential`, :class:`Partial`,
    and :class:`LocatedDifferential` classes.

    :param expression: an expression with one variable
    :param compute_early: whether to do extra work on initialization to have faster evaluation afterwards
    """

    def __init__(
        self: Derivative,
        expression: Expression,
        compute_early: bool = False
    ) -> None:
        exception_message = (
            "Can only take the derivative of an expression with one variable. " +
            "Consider a Differential, Partial, or LocatedDifferential instead."
        )
        variable_name = be.get_the_single_variable_name(expression, exception_message)
        self._original_expression: Expression
        self._original_expression = expression
        self._variable_name: str
        self._variable_name = variable_name
        self._partial: Partial
        self._partial = pa.Partial(expression, variable_name, compute_early = compute_early)

    def at(
        self: Derivative,
        point: Point | float
    ) -> float:
        """
        Evaluates the derivative.

        :param point: where to evaluate the derivative
        """
        if not isinstance(point, pt.Point):
            point = pt.point_on_number_line(self._variable_name, point)
        return self._partial.at(point)

    def as_expression(
        self: Derivative
    ) -> Expression:
        """
        Writes the derivative as an expression.

        NOTE: Writing the derivative as an expression may enlargen the domain.
        For example, ``Derivative(Logarithm(Variable("x")))`` is not defined at negative numbers,
        but as an expression, ``Reciprocal(Variable("x"))`` is defined at negative numbers.
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
        return hash(("Derivative", self._original_expression))

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
