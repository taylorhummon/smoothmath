from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import smoothmath._private.base_expression as base
import smoothmath._private.expression as ex
import smoothmath._private.math_functions as mf
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression
    from smoothmath._private.accumulators import (
        NumericPartialsAccumulator, SyntheticPartialsAccumulator
    )


class Minus(base.BinaryExpression):
    """
    Subtraction.

    >>> from smoothmath import Point
    >>> from smoothmath.expression import Variable, Minus
    >>> Minus(Variable("x"), Variable("y")).at(Point(x=7, y=2))
    5.0

    :param left: the expression being subtracted from
    :param right: the expression being subtracted
    """

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Minus,
        left_value: RealNumber,
        right_value: RealNumber
    ) -> None:
        pass

    def _value_formula(
        self: Minus,
        left_value: RealNumber,
        right_value: RealNumber
    ) -> RealNumber:
        return mf.minus(left_value, right_value)

    ## Partials ##

    def _numeric_partial(
        self: Minus,
        variable_name: str,
        point: Point
    ) -> RealNumber:
        left_partial = self._left._numeric_partial(variable_name, point)
        right_partial = self._right._numeric_partial(variable_name, point)
        return mf.minus(left_partial, right_partial)

    def _synthetic_partial(
        self: Minus,
        variable_name: str
    ) -> Expression:
        left_partial = self._left._synthetic_partial(variable_name)
        right_partial = self._right._synthetic_partial(variable_name)
        return ex.Minus(left_partial, right_partial)

    def _compute_numeric_partials(
        self: Minus,
        accumulator: NumericPartialsAccumulator,
        multiplier: RealNumber,
        point: Point
    ) -> None:
        self._left._compute_numeric_partials(accumulator, multiplier, point)
        self._right._compute_numeric_partials(accumulator, mf.negation(multiplier), point)

    def _compute_synthetic_partials(
        self: Minus,
        accumulator: SyntheticPartialsAccumulator,
        multiplier: Expression
    ) -> None:
        self._left._compute_synthetic_partials(accumulator, multiplier)
        self._right._compute_synthetic_partials(accumulator, ex.Negation(multiplier))

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Minus
    ) -> list[Callable[[], Optional[Expression]]]:
        return [self._reduce_minus_to_sum_with_negation]

    # Minus(u, v) => Add(u, Negation(v))
    def _reduce_minus_to_sum_with_negation(
        self: Minus
    ) -> Optional[Expression]:
        return ex.Add(self._left, ex.Negation(self._right))
