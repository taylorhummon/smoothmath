from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.all_partials import AllPartials
    from smoothmath.expression import Expression

from smoothmath.expression import BinaryExpression
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
import smoothmath.expressions as ex


class Divide(BinaryExpression):
    def __init__(
        self: Divide,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _verify_domain_constraints(
        self: Divide,
        a_value: real_number,
        b_value: real_number
    ) -> None:
        if b_value == 0:
            if a_value == 0:
                raise DomainError("Divide(x, y) is not smooth around (x = 0, y = 0)")
            else: # a_value != 0
                raise DomainError("Divide(x, y) blows up around x != 0 and y = 0")

    def _evaluate(
        self: Divide,
        variable_values: VariableValues
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(variable_values)
        # Note: 0 / b is smooth at b = 0 despite a / b not being smooth at (0, 0)
        if self._a._lacks_variables and a_value == 0:
            self._value = 0
        else:
            b_value = self._b._evaluate(variable_values)
            self._verify_domain_constraints(a_value, b_value)
            self._value = a_value / b_value
        return self._value

    def _partial_at(
        self: Divide,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(variable_values)
        # Note: 0 / b is smooth at b = 0 despite a / b not being smooth at (0, 0)
        if self._a._lacks_variables and a_value == 0:
            return 0
        else:
            b_value = self._b._evaluate(variable_values)
            self._verify_domain_constraints(a_value, b_value)
            a_partial = self._a._partial_at(variable_values, with_respect_to)
            b_partial = self._b._partial_at(variable_values, with_respect_to)
            # d(a / b) = (1 / b) * da - (a / b ** 2) * db
            return (b_value * a_partial - a_value * b_partial) / b_value ** 2

    def _compute_all_partials_at(
        self: Divide,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        a_value = self._a._evaluate(variable_values)
        # Note: 0 / b is smooth at b = 0 despite a / b not being smooth at (0, 0)
        if self._a._lacks_variables and a_value == 0:
            return
        else:
            b_value = self._b._evaluate(variable_values)
            self._verify_domain_constraints(a_value, b_value)
            # d(a / b) = (1 / b) * da - (a / b ** 2) * db
            next_seedA = seed / b_value
            next_seedB =  - seed * a_value / (b_value ** 2)
            self._a._compute_all_partials_at(all_partials, variable_values, next_seedA)
            self._b._compute_all_partials_at(all_partials, variable_values, next_seedB)

    def _synthetic_partial(
        self: Divide,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        # Note: 0 / b is smooth at b = 0 despite a / b not being smooth at (0, 0)
        if self._a._lacks_variables and self._a._evaluate(VariableValues({})) == 0:
            # Note: 0 * b will evaluate to zero unless b is undefined
            return ex.Constant(0)
        else:
            b_partial = self._b._synthetic_partial(with_respect_to)
            return (
                ex.Divide(
                    ex.Minus(
                        ex.Multiply(self._b, a_partial),
                        ex.Multiply(self._a, b_partial)
                    ),
                    ex.Power(self._b, ex.Constant(2))
                )
            )
