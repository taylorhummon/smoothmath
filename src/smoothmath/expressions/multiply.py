from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.typing import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
    from smoothmath.expressions.expression import Expression
from smoothmath.expressions.binary_expression import BinaryExpression

class Multiply(BinaryExpression):
    def __init__(
        self: Multiply,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Multiply,
        variable_values: VariableValues
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self.a._evaluate(variable_values)
        b_value = self.b._evaluate(variable_values)
        self._value = a_value * b_value
        return self._value

    def _partial_at(
        self: Multiply,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_value = self.a._evaluate(variable_values)
        b_value = self.b._evaluate(variable_values)
        a_partial = self.a._partial_at(variable_values, with_respect_to)
        b_partial = self.b._partial_at(variable_values, with_respect_to)
        # d(a * b) = b * da + a * db
        return b_value * a_partial + a_value * b_partial

    def _compute_all_partials_at(
        self: Multiply,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        a_value = self.a._evaluate(variable_values)
        b_value = self.b._evaluate(variable_values)
        # d(a * b) = b * da + a * db
        self.a._compute_all_partials_at(all_partials, variable_values, seed * b_value)
        self.b._compute_all_partials_at(all_partials, variable_values, seed * a_value)
