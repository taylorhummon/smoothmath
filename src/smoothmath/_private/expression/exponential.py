from __future__ import annotations
from typing import Callable
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import exponential, logarithm, multiply


class Exponential(base.ParameterizedUnaryExpression):
    def __init__(
        self: Exponential,
        inner: sm.Expression,
        base: sm.real_number = math.e
    ) -> None:
        super().__init__(inner, base)
        if base <= 0:
            raise Exception(f"Exponential(x) must have a positive base, found: {base}")

    @property
    def base(
        self: Exponential
    ) -> sm.real_number:
        return self._parameter

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Exponential,
        inner_value: sm.real_number
    ) -> None:
        pass

    def _value_formula(
        self: Exponential,
        inner_value: sm.real_number
    ):
        return exponential(inner_value, base = self.base)

    ## Partials and Differentials ##

    def _local_partial_formula(
        self: Exponential,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        if self.base == 1:
            return 0
        self_value = self._evaluate(point)
        if self.base == math.e:
            return multiply(self_value, multiplier)
        else:
            return multiply(
                logarithm(self.base, base = math.e),
                self_value,
                multiplier
            )

    def _synthetic_partial_formula(
        self: Exponential,
        multiplier: sm.Expression
    ) -> sm.Expression:
        if self.base == 1:
            return ex.Constant(0)
        elif self.base == math.e:
            return ex.Multiply(self, multiplier)
        else:
            return ex.Multiply(
                ex.Logarithm(ex.Constant(self.base), base = math.e),
                self,
                multiplier
            )

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Exponential
    ) -> list[Callable[[], sm.Expression | None]]:
        return [
            self._reduce_exponential_of_logarithm_of_u,
            self._reduce_exponential_of_negation_of_u
        ]

    # Exponential(Logarithm(u)) => u
    def _reduce_exponential_of_logarithm_of_u(
        self: Exponential
    ) -> sm.Expression | None:
        if (
            isinstance(self._inner, ex.Logarithm) and
            self.base == self._inner.base
        ):
            return self._inner._inner
        else:
            return None

    # Exponential(Negation(u)) => Reciprocal(Exponential(u))
    def _reduce_exponential_of_negation_of_u(
        self: Exponential
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.Negation):
            return ex.Reciprocal(ex.Exponential(self._inner._inner, base = self.base))
        else:
            return None
