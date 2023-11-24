from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.synthetic import Synthetic
    from smoothmath.all_partials import AllPartials
    from smoothmath.expression import Expression

from smoothmath.expression import BinaryExpression
import smoothmath.expressions as ex


# differential rule: d(a + b) = da + db

class Plus(BinaryExpression):
    def __init__(
        self: Plus,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Plus,
        variable_values: VariableValues
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(variable_values)
        b_value = self._b._evaluate(variable_values)
        self._value = a_value + b_value
        return self._value

    def _partial_at(
        self: Plus,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_partial = self._a._partial_at(variable_values, with_respect_to)
        b_partial = self._b._partial_at(variable_values, with_respect_to)
        return a_partial + b_partial

    def _compute_all_partials_at(
        self: Plus,
        all_partials: AllPartials,
        variable_values: VariableValues,
        accumulated: real_number
    ) -> None:
        self._a._compute_all_partials_at(all_partials, variable_values, accumulated)
        self._b._compute_all_partials_at(all_partials, variable_values, accumulated)

    def _synthetic_partial(
        self: Plus,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        b_partial = self._b._synthetic_partial(with_respect_to)
        return ex.Plus(a_partial, b_partial)

    def _compute_all_synthetic_partials(
        self: Plus,
        synthetic: Synthetic,
        accumulated: Expression
    ) -> None:
        self._a._compute_all_synthetic_partials(synthetic, accumulated)
        self._b._compute_all_synthetic_partials(synthetic, accumulated)
