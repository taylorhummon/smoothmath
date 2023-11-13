from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.typing import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
    from smoothmath.expressions.expression import Expression
import math
from smoothmath.errors import DomainError
from smoothmath.expressions.unary_expression import UnaryExpression

class SquareRoot(UnaryExpression):
    def __init__(
        self: SquareRoot,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: SquareRoot,
        variable_values: VariableValues
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self.a._evaluate(variable_values)
        self._ensure_value_is_in_domain(a_value)
        self._value = math.sqrt(a_value)
        return self._value

    def _partial_at(
        self: SquareRoot,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_value = self.a._evaluate(variable_values)
        self._ensure_value_is_in_domain(a_value)
        a_partial = self.a._partial_at(variable_values, with_respect_to)
        # d(sqrt(a)) = (1 / (2 sqrt(a))) * da
        return a_partial / (2 * math.sqrt(a_value))

    def _compute_all_partials_at(
        self: SquareRoot,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        a_value = self.a._evaluate(variable_values)
        self._ensure_value_is_in_domain(a_value)
        self_value = self._evaluate(variable_values)
        # d(sqrt(a)) = (1 / (2 sqrt(a))) * da
        next_seed = seed / (2 * self_value)
        self.a._compute_all_partials_at(all_partials, variable_values, next_seed)

    def _ensure_value_is_in_domain(
        self: SquareRoot,
        a_value: real_number
    ) -> None:
        if a_value == 0:
            raise DomainError("SquareRoot(x) is not smooth around x = 0")
        elif a_value < 0:
            raise DomainError("SquareRoot(x) is undefined for x < 0")
