from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.typing import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
    from smoothmath.expressions.expression import Expression
import math
from smoothmath.expressions.unary_expression import UnaryExpression

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
        a_value = self.a._evaluate(variable_values)
        self._value = math.cos(a_value)
        return self._value

    def _partial_at(
        self: Cosine,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_value = self.a._evaluate(variable_values)
        a_partial = self.a._partial_at(variable_values, with_respect_to)
        # d(cos(a)) = - sin(a) * da
        return - math.sin(a_value) * a_partial

    def _compute_all_partials_at(
        self: Cosine,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        a_value = self.a._evaluate(variable_values)
        # d(cos(a)) = - sin(a) * da
        next_seed = - seed * math.sin(a_value)
        self.a._compute_all_partials_at(all_partials, variable_values, next_seed)
