from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
    from smoothmath.expression import Expression

import math
from smoothmath.expression import UnaryExpression
import smoothmath.expressions as ex


class Exponential(UnaryExpression):
    def __init__(
        self: Exponential,
        exponent: Expression,
        base: real_number = math.e
    ) -> None:
        super().__init__(exponent)
        if base <= 0:
            raise Exception("Exponentials must have a positive base")
        self._base: real_number
        self._base = base

    def _evaluate(
        self: Exponential,
        variable_values: VariableValues
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(variable_values)
        self._value = self._base ** a_value
        return self._value

    def _partial_at(
        self: Exponential,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(variable_values)
        a_partial = self._a._partial_at(variable_values, with_respect_to)
        resultValue = self._base ** a_value
        # d(C ** a) = ln(C) * C ** a * da
        return math.log(self._base) * resultValue * a_partial

    def _compute_all_partials_at(
        self: Exponential,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        self_value = self._evaluate(variable_values)
        # d(C ** a) = ln(C) * C ** a * da
        next_seed = seed * math.log(self._base) * self_value
        self._a._compute_all_partials_at(all_partials, variable_values, next_seed)

    def _synthetic_partial(
        self: Exponential,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return ex.Multiply(
            ex.Multiply(
                ex.Logarithm(ex.Constant(self._base)),
                ex.Exponential(self._a, self._base)
            ),
            a_partial
        )
