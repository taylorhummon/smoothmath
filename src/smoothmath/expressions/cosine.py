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


class Cosine(UnaryExpression):
    def __init__(
        self: Cosine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Cosine,
        variable_values: VariableValues
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(variable_values)
        self._value = math.cos(a_value)
        return self._value

    def _partial_at(
        self: Cosine,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(variable_values)
        a_partial = self._a._partial_at(variable_values, with_respect_to)
        # d(cos(a)) = - sin(a) * da
        return - math.sin(a_value) * a_partial

    def _compute_all_partials_at(
        self: Cosine,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        a_value = self._a._evaluate(variable_values)
        # d(cos(a)) = - sin(a) * da
        next_seed = - seed * math.sin(a_value)
        self._a._compute_all_partials_at(all_partials, variable_values, next_seed)

    def _synthetic_partial(
        self: Cosine,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return ex.Multiply(
            ex.Negation(ex.Sine(self._a)),
            a_partial
        )
