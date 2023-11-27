from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.computed_local_partials import ComputedLocalPartials
    from smoothmath.synthetic import Synthetic
    from smoothmath.expression import Expression

import math
from smoothmath.expression import BinaryExpression
from smoothmath.errors import DomainError
from smoothmath.point import Point
import smoothmath.utilities as utilities
import smoothmath.expressions as ex


# For a power, a ** b, there are two over-arching cases we work with:
# (i) the exponent, b, can be determined to be a constant integer
#     e.g. a ** 2, a ** 3, or a ** (-1)
# (ii) otherwise
#     e.g. e ** b, or 3 ** b, a ** b,
# In case (i), we allow negative bases. In case (i), we only allow positive bases.


def _is_case_i(
    b: Expression
) -> bool:
    return b._lacks_variables and utilities.is_integer(b.evaluate(Point({})))


# differential rule: d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db

class Power(BinaryExpression):
    def __init__(
        self: Power,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Power,
        point: Point
    ) -> real_number:
        if _is_case_i(self._b):
            return self._evaluate_case_i(point)
        else:
            return self._evaluate_case_ii(point)

    def _partial_at(
        self: Power,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        if _is_case_i(self._b):
            return self._partial_at_case_i(point, with_respect_to)
        else:
            return self._partial_at_case_ii(point, with_respect_to)

    def _compute_local_partials(
        self: Power,
        computed_local_partials: ComputedLocalPartials,
        point: Point,
        accumulated: real_number
    ) -> None:
        if _is_case_i(self._b):
            self._compute_local_partials_case_i(computed_local_partials, point, accumulated)
        else:
            self._compute_local_partials_case_ii(computed_local_partials, point, accumulated)

    def _synthetic_partial(
        self: Power,
        with_respect_to: str
    ) -> Expression:
        if _is_case_i(self._b):
            return self._synthetic_partial_case_i(with_respect_to)
        else:
            return self._synthetic_partial_case_ii(with_respect_to)

    def _compute_all_synthetic_partials(
        self: Power,
        synthetic: Synthetic,
        accumulated: Expression
    ) -> None:
        if _is_case_i(self._b):
            self._compute_all_synthetic_partials_case_i(synthetic, accumulated)
        else:
            self._compute_all_synthetic_partials_case_ii(synthetic, accumulated)

    ### CASE i ###

    def _verify_domain_constraints_case_i(
        self: Power,
        a_value: real_number,
        b_value: real_number
    ) -> None:
        if a_value == 0:
            if b_value == 0:
                raise DomainError("Power(x, y) is not smooth around (x = 0, y = 0)")
            elif b_value <= -1:
                raise DomainError("Power(x, Constant(c)) blows up around x = 0 when c is a negative integer")

    def _evaluate_case_i(
        self: Power,
        point: Point
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        b_value = self._b._evaluate(point) # b_value is an integer (this is case i)
        self._verify_domain_constraints_case_i(a_value, b_value)
        if b_value == 0:
            self._value = 1
        else: # b_value is non-zero
            self._value = a_value ** b_value
        return self._value

    def _partial_at_case_i(
        self: Power,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(point)
        b_value = self._b._evaluate(point) # b_value is an integer (this is case i)
        self._verify_domain_constraints_case_i(a_value, b_value)
        if b_value == 0:
            # d(a ** 0) = 0 * da
            return 0
        elif b_value == 1:
            # d(a ** 1) = 1 * da
            return self._a._partial_at(point, with_respect_to)
        else: # b_value >= 2 or b_value <= -1
            a_partial = self._a._partial_at(point, with_respect_to)
            # d(a ** C) = C * a ** (C - 1) * da
            return b_value * (a_value ** (b_value - 1)) * a_partial

    def _compute_local_partials_case_i(
        self: Power,
        computed_local_partials: ComputedLocalPartials,
        point: Point,
        accumulated: real_number
    ) -> None:
        a_value = self._a._evaluate(point)
        b_value = self._b._evaluate(point) # b_value is an integer (this is case i)
        self._verify_domain_constraints_case_i(a_value, b_value)
        if b_value == 0:
            # d(a ** 0) = 0 * da
            return
        elif b_value == 1:
            # d(a ** 1) = da
            self._a._compute_local_partials(computed_local_partials, point, accumulated)
        else: # b_value >= 2 or b_value <= -1
            # d(a ** C) = C * a ** (C - 1) * da
            next_accumulated = accumulated * b_value * (a_value ** (b_value - 1))
            self._a._compute_local_partials(computed_local_partials, point, next_accumulated)

    def _synthetic_partial_case_i(
        self: Power,
        with_respect_to: str
    ) -> Expression:
        b_value = self._b._evaluate(Point({})) # b_value is an integer (this is case i)
        if b_value == 0:
            return ex.Constant(0)
        elif b_value == 1:
            # d(a ** 1) = 1 * da
            return self._a._synthetic_partial(with_respect_to)
        else: # b_value >= 2 or b_value <= -1
            # d(a ** C) = C * a ** (C - 1) * da
            return self._term_1(self._a._synthetic_partial(with_respect_to))

    def _compute_all_synthetic_partials_case_i(
        self: Power,
        synthetic: Synthetic,
        accumulated: Expression
    ) -> None:
        b_value = self._b._evaluate(Point({})) # b_value is an integer (this is case i)
        if b_value == 0:
            # d(a ** 0) = 0 * da
            return
        elif b_value == 1:
            # d(a ** 1) = da
            self._a._compute_all_synthetic_partials(synthetic, accumulated)
        else: # b_value >= 2 or b_value <= -1
            # d(a ** C) = C * a ** (C - 1) * da
            self._a._compute_all_synthetic_partials(synthetic, self._term_1(accumulated))

    ### CASE ii ###

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

    def _evaluate_case_ii(
        self: Power,
        point: Point
    ) -> real_number:
        if self._value is not None:
            return self._value
        if self._a._lacks_variables and self._a._evaluate(point) == 1:
            # If we find something like, Constant(1) ** Variable("b"), we can short-circuit.
            self._value = 1
        else:
            a_value = self._a._evaluate(point)
            b_value = self._b._evaluate(point)
            self._verify_domain_constraints_case_ii(a_value, b_value)
            self._value = a_value ** b_value
        return self._value

    def _partial_at_case_ii(
        self: Power,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        if self._a._lacks_variables and self._a._evaluate(point) == 1:
            # If we find something like, Constant(1) ** Variable("b"), we can short-circuit.
            return 0
        else:
            a_value = self._a._evaluate(point)
            b_value = self._b._evaluate(point)
            self._verify_domain_constraints_case_ii(a_value, b_value)
            a_partial = self._a._partial_at(point, with_respect_to)
            b_partial = self._b._partial_at(point, with_respect_to)
            # d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db
            return (
                b_value * (a_value ** (b_value - 1)) * a_partial +
                math.log(a_value) * (a_value ** b_value) * b_partial
            )

    def _compute_local_partials_case_ii(
        self: Power,
        computed_local_partials: ComputedLocalPartials,
        point: Point,
        accumulated: real_number
    ) -> None:
        if self._a._lacks_variables and self._a._evaluate(point) == 1:
            # If we find something like, Constant(1) ** Variable("b"), we can short-circuit.
            pass
        else:
            a_value = self._a._evaluate(point)
            b_value = self._b._evaluate(point)
            self._verify_domain_constraints_case_ii(a_value, b_value)
            # d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db
            next_accumulated_a = accumulated * b_value * a_value ** (b_value - 1)
            next_accumulated_b = accumulated * math.log(a_value) * a_value ** b_value
            self._a._compute_local_partials(computed_local_partials, point, next_accumulated_a)
            self._b._compute_local_partials(computed_local_partials, point, next_accumulated_b)

    def _synthetic_partial_case_ii(
        self: Power,
        with_respect_to: str
    ) -> Expression:
        return ex.Plus(
            self._term_1(self._a._synthetic_partial(with_respect_to)),
            self._term_2(self._b._synthetic_partial(with_respect_to))
        )

    def _compute_all_synthetic_partials_case_ii(
        self: Power,
        synthetic: Synthetic,
        accumulated: Expression
    ) -> None:
        self._a._compute_all_synthetic_partials(synthetic, self._term_1(accumulated))
        self._b._compute_all_synthetic_partials(synthetic, self._term_2(accumulated))

    def _term_1(
        self: Power,
        multiplier: Expression
    ) -> Expression:
        return ex.Multiply(
            ex.Multiply(self._b, ex.Power(self._a, ex.Minus(self._b, ex.Constant(1)))),
            multiplier
        )

    def _term_2(
        self: Power,
        multiplier: Expression
    ) -> Expression:
        return ex.Multiply(
            ex.Multiply(ex.Logarithm(self._a), ex.Power(self._a, self._b)),
            multiplier
        )
