from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.typing import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
    from smoothmath.expressions.expression import Expression

# imports needed for class declaration
from smoothmath.expressions.unary_expression import UnaryExpression
import math

class Logarithm(UnaryExpression):
    def __init__(
        self: Logarithm,
        a: Expression,
        base: real_number = math.e
    ) -> None:
        super().__init__(a)
        if base <= 0:
            raise Exception("Logarithms must have a positive base")
        elif base == 1:
            raise Exception("Logarithms cannot have base = 1")
        self._base : real_number
        self._base = base

    def _evaluate(
        self: Logarithm,
        variable_values: VariableValues
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(variable_values)
        self._ensure_value_is_in_domain(a_value)
        self._value = math.log(a_value, self._base)
        return self._value

    def _partial_at(
        self: Logarithm,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(variable_values)
        a_partial = self._a._partial_at(variable_values, with_respect_to)
        self._ensure_value_is_in_domain(a_value)
        # d(log_C(a)) = (1 / (ln(C) * a)) * da
        return a_partial / (math.log(self._base) * a_value)

    def _compute_all_partials_at(
        self: Logarithm,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        a_value = self._a._evaluate(variable_values)
        self._ensure_value_is_in_domain(a_value)
        # d(log_C(a)) = (1 / (ln(C) * a)) * da
        next_seed = seed / (math.log(self._base) * a_value)
        self._a._compute_all_partials_at(all_partials, variable_values, next_seed)

    def _ensure_value_is_in_domain(
        self: Logarithm,
        a_value: real_number
    ) -> None:
        if a_value == 0:
            raise DomainError("Logarithm(x) blows up around x = 0")
        elif a_value < 0:
            raise DomainError("Logarithm(x) is undefined for x < 0")

# imports needed for class implementation
from smoothmath.errors import DomainError
