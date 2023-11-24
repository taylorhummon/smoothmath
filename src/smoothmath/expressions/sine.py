from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
    from smoothmath.synthetic import Synthetic
    from smoothmath.expression import Expression

import math
from smoothmath.expression import UnaryExpression
import smoothmath.expressions as ex


# differential rule: d(sin(a)) = cos(a) * da

class Sine(UnaryExpression):
    def __init__(
        self: Sine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Sine,
        variable_values: VariableValues
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(variable_values)
        self._value = math.sin(a_value)
        return self._value

    def _partial_at(
        self: Sine,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(variable_values)
        a_partial = self._a._partial_at(variable_values, with_respect_to)
        return math.cos(a_value) * a_partial

    def _compute_all_partials_at(
        self: Sine,
        all_partials: AllPartials,
        variable_values: VariableValues,
        accumulated: real_number
    ) -> None:
        a_value = self._a._evaluate(variable_values)
        next_accumulated = accumulated * math.cos(a_value)
        self._a._compute_all_partials_at(all_partials, variable_values, next_accumulated)

    def _synthetic_partial(
        self: Sine,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return ex.Multiply(
            ex.Cosine(self._a),
            a_partial
        )

    def _compute_all_synthetic_partials(
        self: Sine,
        synthetic: Synthetic,
        accumulated: Expression
    ) -> None:
        next_accumulated = ex.Multiply(accumulated, ex.Cosine(self._a))
        self._a._compute_all_synthetic_partials(synthetic, next_accumulated)
