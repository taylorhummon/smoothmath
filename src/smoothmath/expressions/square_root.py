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
from smoothmath.errors import DomainError
import smoothmath.expressions as ex


# differential rule: d(sqrt(a)) = (1 / (2 sqrt(a))) * da

class SquareRoot(UnaryExpression):
    def __init__(
        self: SquareRoot,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _verify_domain_constraints(
        self: SquareRoot,
        a_value: real_number
    ) -> None:
        if a_value == 0:
            raise DomainError("SquareRoot(x) is not smooth around x = 0")
        elif a_value < 0:
            raise DomainError("SquareRoot(x) is undefined for x < 0")

    def _evaluate(
        self: SquareRoot,
        variable_values: VariableValues
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(variable_values)
        self._verify_domain_constraints(a_value)
        self._value = math.sqrt(a_value)
        return self._value

    def _partial_at(
        self: SquareRoot,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(variable_values)
        self._verify_domain_constraints(a_value)
        a_partial = self._a._partial_at(variable_values, with_respect_to)
        return a_partial / (2 * math.sqrt(a_value))

    def _compute_all_partials_at(
        self: SquareRoot,
        all_partials: AllPartials,
        variable_values: VariableValues,
        accumulated: real_number
    ) -> None:
        a_value = self._a._evaluate(variable_values)
        self._verify_domain_constraints(a_value)
        self_value = self._evaluate(variable_values)
        next_accumulated = accumulated / (2 * self_value)
        self._a._compute_all_partials_at(all_partials, variable_values, next_accumulated)

    def _synthetic_partial(
        self: SquareRoot,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return self._synthetic_partial_helper(a_partial)

    def _compute_all_synthetic_partials(
        self: SquareRoot,
        synthetic: Synthetic,
        accumulated: Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_helper(accumulated)
        self._a._compute_all_synthetic_partials(synthetic, next_accumulated)

    def _synthetic_partial_helper(
        self: SquareRoot,
        multiplier: Expression
    ) -> Expression:
        return ex.Divide(
            multiplier,
            ex.Multiply(ex.Constant(2), ex.SquareRoot(self._a))
        )
