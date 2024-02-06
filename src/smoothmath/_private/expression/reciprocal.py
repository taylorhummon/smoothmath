from __future__ import annotations
from typing import Callable
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import negation, reciprocal, nth_power, divide


class Reciprocal(base.UnaryExpression):

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Reciprocal,
        inner_value: sm.real_number
    ) -> None:
        if inner_value == 0:
            raise sm.DomainError("Reciprocal(x) blows up around x = 0")

    def _value_formula(
        self: Reciprocal,
        inner_value: sm.real_number
    ):
        return reciprocal(inner_value)

    ## Partials and Differentials ##

    def _local_partial_formula(
        self: Reciprocal,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        inner_value = self._inner._evaluate(point)
        return negation(divide(multiplier, nth_power(inner_value, n = 2)))

    def _synthetic_partial_formula(
        self: Reciprocal,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Negation(ex.Divide(multiplier, ex.NthPower(self._inner, n = 2)))

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Reciprocal
    ) -> list[Callable[[], sm.Expression | None]]:
        return [
            self._reduce_reciprocal_of_reciprocal,
            self._reduce_reciprocal_of_negation,
            self._reduce_reciprocal_of_product
        ]

    # Reciprocal(Reciprocal(u)) => u
    def _reduce_reciprocal_of_reciprocal(
        self: Reciprocal
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.Reciprocal):
            return self._inner._inner
        else:
            return None

    # Reciprocal(Negation(u)) => Negation(Reciprocal(u))
    def _reduce_reciprocal_of_negation(
        self: Reciprocal
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.Negation):
            return ex.Negation(ex.Reciprocal(self._inner._inner))
        else:
            return None

    # Reciprocal(Multiply(u, v)) => Multiply(Reciprocal(u), Reciprocal(v))
    def _reduce_reciprocal_of_product(
        self: Reciprocal
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.Multiply):
            return ex.Multiply(*(Reciprocal(inner) for inner in self._inner._inners))
        else:
            return None
