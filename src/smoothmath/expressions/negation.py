from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.typing import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
    from smoothmath.expressions.expression import Expression

# imports needed for class declaration
from smoothmath.expressions.unary_expression import UnaryExpression

class Negation(UnaryExpression):
    def __init__(
        self: Negation,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Negation,
        variable_values: VariableValues
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(variable_values)
        self._value = - a_value
        return self._value

    def _partial_at(
        self: Negation,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_partial = self._a._partial_at(variable_values, with_respect_to)
        # d(-a) = -da
        return - a_partial

    def _compute_all_partials_at(
        self: Negation,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        # d(-a) = -da
        self._a._compute_all_partials_at(all_partials, variable_values, - seed)
