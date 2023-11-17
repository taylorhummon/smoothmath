from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
    from smoothmath.expression import Expression

import math
from smoothmath.expression import BinaryExpression
from smoothmath.errors import DomainError
import smoothmath.utilities as utilities
import smoothmath.expressions as ex

# For a power, a ** b, there are two over-arching cases we work with:
# (i) the exponent, b, can be determined to be a constant integer
#     e.g. a ** 2, a ** 3, or a ** (-1)
# (ii) otherwise
#     e.g. e ** b, or 3 ** b, a ** b,
# In case (i), we allow negative bases. In case (i), we only allow positive bases.


def _is_case_i(
    b: Expression,
    variable_values: VariableValues
) -> bool:
    if not b._lacks_variables:
        return False
    b_value = b.evaluate(variable_values)
    return utilities.is_integer(b_value)


class Power(BinaryExpression):
    def __init__(
        self: Power,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _verify_domain_constraints_case_i(
        self: Power,
        a_value: real_number,
        b_value: real_number
    ) -> None:
        if a_value == 0 and b_value <= -1:
            raise DomainError("Power(x, Constant(c)) blows up around x = 0 when c is a negative integer")

    def _verify_domain_constraints_case_ii(
        self: Power,
        a_value: real_number,
        b_value: real_number
    ) -> None:
        if a_value == 0:
            if b_value > 0:
                raise DomainError("Power(x, y) is not smooth around x = 0 for y > 0")
            elif b_value == 0:
                raise DomainError("Power(x, y) is not smooth around (x = 0, y = 0)")
            else: # b_value < 0
                raise DomainError("Power(x, y) blows up around x = 0 for y < 0")
        elif a_value < 0:
            raise DomainError("Power(x, y) is undefined for x < 0")

    def _evaluate(
        self: Power,
        variable_values: VariableValues
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(variable_values)
        b_value = self._b._evaluate(variable_values)
        if _is_case_i(self._b, variable_values):
            self._verify_domain_constraints_case_i(a_value, b_value)
        else: # case ii
            self._verify_domain_constraints_case_ii(a_value, b_value)
        self._value = a_value ** b_value
        return self._value

    def _partial_at(
        self: Power,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(variable_values)
        b_value = self._b._evaluate(variable_values)
        a_partial = self._a._partial_at(variable_values, with_respect_to)
        b_partial = self._b._partial_at(variable_values, with_respect_to)
        if _is_case_i(self._b, variable_values):
            self._verify_domain_constraints_case_i(a_value, b_value)
            return self._partial_case_i(a_value, a_partial, b_value)
        else: # case ii
            self._verify_domain_constraints_case_ii(a_value, b_value)
            return self._partial_case_ii(a_value, a_partial, b_value, b_partial)

    def _partial_case_i(
        self: Power,
        a_value: real_number,
        a_partial: real_number,
        b_value: real_number
    ) -> real_number:
        if b_value == 0:
            # Note: x ** 0 is smooth at x = 0 despite x ** y not being smooth at (0, 0)
            # d(a ** 0) = 0 * da
            return 0
        elif b_value == 1:
            # d(a ** 1) = 1 * da
            return a_partial
        else: # b_value >= 2 or b_value <= -1
            # d(a ** C) = C * a ** (C - 1) * da
            return b_value * (a_value ** (b_value - 1)) * a_partial

    def _partial_case_ii(
        self,
        a_value: real_number,
        a_partial: real_number,
        b_value: real_number,
        b_partial: real_number
    ) -> real_number:
        # d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db
        return (
            b_value * (a_value ** (b_value - 1)) * a_partial +
            math.log(a_value) * (a_value ** b_value) * b_partial
        )

    def _compute_all_partials_at(
        self: Power,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        a_value = self._a._evaluate(variable_values)
        b_value = self._b._evaluate(variable_values)
        if _is_case_i(self._b, variable_values):
            self._verify_domain_constraints_case_i(a_value, b_value)
            next_seed = self._next_seed_case_i(a_value, b_value, seed)
            self._a._compute_all_partials_at(all_partials, variable_values, next_seed)
        else: # case ii
            self._verify_domain_constraints_case_ii(a_value, b_value)
            # d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db
            next_seed_a = self._next_seed_a_case_ii(a_value, b_value, seed)
            next_seed_b = self._next_seed_b_case_ii(a_value, b_value, seed)
            self._a._compute_all_partials_at(all_partials, variable_values, next_seed_a)
            self._b._compute_all_partials_at(all_partials, variable_values, next_seed_b)

    def _next_seed_case_i(
        self: Power,
        a_value: real_number,
        b_value: real_number,
        seed: real_number
    ) -> real_number:
        if b_value == 0:
            # Note: a ** 0 is smooth at a = 0 despite a ** b not being smooth at (0, 0)
            # d(a ** 0) = 0 * da
            return 0
        elif b_value == 1:
            # d(a ** 1) = da
            return seed
        else: # b_value >= 2 or b_value <= -1
            # d(a ** C) = C * a ** (C - 1) * da
            return seed * b_value * (a_value ** (b_value - 1))

    def _next_seed_a_case_ii(
        self: Power,
        a_value: real_number,
        b_value: real_number,
        seed: real_number
    ) -> real_number:
        return seed * b_value * a_value ** (b_value - 1)

    def _next_seed_b_case_ii(
        self: Power,
        a_value: real_number,
        b_value: real_number,
        seed: real_number
    ) -> real_number:
        return seed * math.log(a_value) * a_value ** b_value

    def _synthetic_partial(
            self: Power,
            with_respect_to: str
        ) -> Expression:
            a_partial = self._a._synthetic_partial(with_respect_to)
            b_partial = self._b._synthetic_partial(with_respect_to)
            term_1 = (
                ex.Multiply(
                    self._b,
                    Power(
                        self._a,
                        ex.Minus(self._b, ex.Constant(1))
                    )
                )
            )
            term_2 = (
                ex.Multiply(
                    ex.Logarithm(self._a),
                    ex.Power(self._a, self._b)
                )
            )
            return (
                ex.Plus(
                    ex.Multiply(term_1, a_partial),
                    ex.Multiply(term_2, b_partial)
                )
            )
