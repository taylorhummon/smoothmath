from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
    from smoothmath.expression import Expression

from smoothmath.expression import BinaryExpression
import smoothmath.expressions as ex


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
        a_value = self._a._evaluate(variable_values)
        b_value = self._b._evaluate(variable_values)
        self._value = a_value * b_value
        return self._value

    def _partial_at(
        self: Multiply,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(variable_values)
        b_value = self._b._evaluate(variable_values)
        a_partial = self._a._partial_at(variable_values, with_respect_to)
        b_partial = self._b._partial_at(variable_values, with_respect_to)
        # d(a * b) = b * da + a * db
        return b_value * a_partial + a_value * b_partial

    def _compute_all_partials_at(
        self: Multiply,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        a_value = self._a._evaluate(variable_values)
        b_value = self._b._evaluate(variable_values)
        # d(a * b) = b * da + a * db
        self._a._compute_all_partials_at(all_partials, variable_values, seed * b_value)
        self._b._compute_all_partials_at(all_partials, variable_values, seed * a_value)

    def _synthetic_partial(
        self: Multiply,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        b_partial = self._b._synthetic_partial(with_respect_to)
        return ex.Plus(
            ex.Multiply(self._b, a_partial),
            ex.Multiply(self._a, b_partial)
        )
