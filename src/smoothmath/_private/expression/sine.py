from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import cosine, sine, multiply
if TYPE_CHECKING:
    from smoothmath import RealNumber


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
        return sine(inner_value)

    ## Partials and Differentials ##

    def _local_partial_formula(
        self: Sine,
        point: sm.Point,
        multiplier: RealNumber
    ) -> RealNumber:
        inner_value = self._inner._evaluate(point)
        return multiply(cosine(inner_value), multiplier)

    def _synthetic_partial_formula(
        self: Sine,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(ex.Cosine(self._inner), multiplier)

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Sine
    ) -> list[Callable[[], Optional[sm.Expression]]]:
        return [self._reduce_sine_of_negation]

    # Sine(Negation(u)) => Negation(Sine(u))
    def _reduce_sine_of_negation(
        self: Sine
    ) -> Optional[sm.Expression]:
        if isinstance(self._inner, ex.Negation):
            return ex.Negation(ex.Sine(self._inner._inner))
        else:
            return None
