from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.local_differential import LocalDifferential
    from smoothmath.global_differential import GlobalDifferential
    from smoothmath.expression import Expression

from smoothmath.expression import BinaryExpression
from smoothmath.errors import DomainError
from smoothmath.point import Point
import smoothmath.expressions as ex


# differential rule: d(a / b) = (1 / b) * da - (a / b ** 2) * db

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
        point: Point
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        b_value = self._b._evaluate(point)
        self._verify_domain_constraints(a_value, b_value)
        self._value = a_value / b_value
        return self._value

    def _local_partial(
        self: Divide,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        a_value = self._a._evaluate(point)
        b_value = self._b._evaluate(point)
        self._verify_domain_constraints(a_value, b_value)
        a_partial = self._a._local_partial(point, with_respect_to)
        b_partial = self._b._local_partial(point, with_respect_to)
        return (b_value * a_partial - a_value * b_partial) / b_value ** 2

    def _synthetic_partial(
        self: Divide,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        b_partial = self._b._synthetic_partial(with_respect_to)
        numerator = ex.Minus(
            ex.Multiply(self._b, a_partial),
            ex.Multiply(self._a, b_partial)
        )
        denominator = ex.Power(self._b, ex.Constant(2))
        return ex.Divide(numerator, denominator)

    def _compute_local_differential(
        self: Divide,
        local_differential: LocalDifferential,
        point: Point,
        accumulated: real_number
    ) -> None:
        a_value = self._a._evaluate(point)
        b_value = self._b._evaluate(point)
        self._verify_domain_constraints(a_value, b_value)
        next_accumulated_a = accumulated / b_value
        next_accumulated_b =  - accumulated * a_value / (b_value ** 2)
        self._a._compute_local_differential(local_differential, point, next_accumulated_a)
        self._b._compute_local_differential(local_differential, point, next_accumulated_b)

    def _compute_global_differential(
        self: Divide,
        global_differential: GlobalDifferential,
        accumulated: Expression
    ) -> None:
        next_accumulated_a = ex.Divide(accumulated, self._b)
        next_accumulated_b = ex.Multiply(
            accumulated,
            ex.Negation(ex.Divide(self._a, ex.Power(self._b, ex.Constant(2))))
        )
        self._a._compute_global_differential(global_differential, next_accumulated_a)
        self._b._compute_global_differential(global_differential, next_accumulated_b)
