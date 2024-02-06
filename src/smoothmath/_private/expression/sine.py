from __future__ import annotations
from typing import Callable
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import cosine, sine, multiply


class Sine(base.UnaryExpression):

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Sine,
        inner_value: sm.real_number
    ) -> None:
        pass

    def _value_formula(
        self: Sine,
        inner_value: sm.real_number
    ) -> sm.real_number:
        return sine(inner_value)

    ## Partials and Differentials ##

    def _local_partial_formula(
        self: Sine,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
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
    ) -> list[Callable[[], sm.Expression | None]]:
        return [self._reduce_sine_of_negation_of_u]

    # Sine(Negation(u)) => Negation(Sine(u))
    def _reduce_sine_of_negation_of_u(
        self: Sine
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.Negation):
            return ex.Negation(ex.Sine(self._inner._inner))
        else:
            return None
