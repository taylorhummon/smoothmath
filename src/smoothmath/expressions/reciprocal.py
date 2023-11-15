from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
    from smoothmath.expression import Expression

from smoothmath.expression import UnaryExpression
from smoothmath.errors import DomainError
import smoothmath.expressions as ex


class Reciprocal(UnaryExpression):
    def __init__(
        self: Reciprocal,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Reciprocal,
        variable_values: VariableValues
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(variable_values)
        self._ensure_value_is_in_domain(a_value)
        self._value = 1 / a_value
        return self._value

    def _partial_at(
        self: Reciprocal,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(variable_values)
        a_partial = self._a._partial_at(variable_values, with_respect_to)
        self._ensure_value_is_in_domain(a_value)
        resultValue = self._evaluate(variable_values)
        # d(1 / a) = - (1 / a ** 2) * da
        return - (resultValue ** 2) * a_partial

    def _compute_all_partials_at(
        self: Reciprocal,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        a_value = self._a._evaluate(variable_values)
        self._ensure_value_is_in_domain(a_value)
        self_value = self._evaluate(variable_values)
        # d(1 / a) = - (1 / a ** 2) * da
        next_seed = - seed * (self_value ** 2)
        self._a._compute_all_partials_at(all_partials, variable_values, next_seed)

    def _ensure_value_is_in_domain(
        self: Reciprocal,
        a_value: real_number
    ) -> None:
        if a_value == 0:
            raise DomainError("Reciprocal(x) blows up around x = 0")

    def _synthetic_partial(
        self: Reciprocal,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return (
            ex.Multiply(
                ex.Negation(ex.Reciprocal(ex.Power(self._a, ex.Constant(2)))),
                a_partial
            )
        )
