from __future__ import annotations
from typing import Callable
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import negation, cosine, sine, multiply


class Cosine(base.UnaryExpression):

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Cosine,
        inner_value: sm.real_number
    ) -> None:
        pass

    def _value_formula(
        self: Cosine,
        inner_value: sm.real_number
    ) -> sm.real_number:
        return cosine(inner_value)

    ## Partials and Differentials ##

    def _local_partial_formula(
        self: Cosine,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        inner_value = self._inner._evaluate(point)
        return multiply(negation(sine(inner_value)), multiplier)

    def _synthetic_partial_formula(
        self: Cosine,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(ex.Negation(ex.Sine(self._inner)), multiplier)

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Cosine
    ) -> list[Callable[[], sm.Expression | None]]:
        return [self._reduce_cosine_of_negation_of_u]

    # Cosine(Negation(u)) => Cosine(u)
    def _reduce_cosine_of_negation_of_u(
        self: Cosine
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.Negation):
            return ex.Cosine(self._inner._inner)
        else:
            return None
