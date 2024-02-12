from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
import smoothmath._private.math_functions as mf
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression


class Sine(base.UnaryExpression):
    """
    The sine of an expression.

    :param inner: an expression representing an angle in radians
    """

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Sine,
        inner_value: RealNumber
    ) -> None:
        pass

    def _value_formula(
        self: Sine,
        inner_value: RealNumber
    ) -> RealNumber:
        return mf.sine(inner_value)

    ## Partials and Differentials ##

    def _local_partial_formula(
        self: Sine,
        point: Point,
        multiplier: RealNumber
    ) -> RealNumber:
        inner_value = self._inner._evaluate(point)
        return mf.multiply(mf.cosine(inner_value), multiplier)

    def _synthetic_partial_formula(
        self: Sine,
        multiplier: Expression
    ) -> Expression:
        return ex.Multiply(ex.Cosine(self._inner), multiplier)

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Sine
    ) -> list[Callable[[], Optional[Expression]]]:
        return [self._reduce_sine_of_negation]

    # Sine(Negation(u)) => Negation(Sine(u))
    def _reduce_sine_of_negation(
        self: Sine
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.Negation):
            return ex.Negation(ex.Sine(self._inner._inner))
        else:
            return None
