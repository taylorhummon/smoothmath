from __future__ import annotations
from typing import TYPE_CHECKING
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


# differential rule: d(a ** b) = b * a ** (b - 1) * da + log_e(a) * a ** b * db

class Power(base.BinaryExpression):
    def __init__(
        self: Power,
        expression_a: sm.Expression,
        expression_b: sm.Expression
    ) -> None:
        super().__init__(expression_a, expression_b)

    def _verify_domain_constraints(
        self: Power,
        a_value: sm.real_number,
        b_value: sm.real_number
    ) -> None:
        if a_value == 0:
            if b_value > 0:
                raise sm.DomainError("Power(x, y) is not smooth around x = 0 for y > 0")
            elif b_value == 0:
                raise sm.DomainError("Power(x, y) is not smooth around (x = 0, y = 0)")
            else: # b_value < 0
                raise sm.DomainError("Power(x, y) blows up around x = 0 for y < 0")
        elif a_value < 0:
            raise sm.DomainError("Power(x, y) is undefined for x < 0")

    def _evaluate(
        self: Power,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        if self._a._lacks_variables and self._a._evaluate(point) == 1:
            # If we find something like, Constant(1) ** Variable("b"), we can short-circuit.
            self._value = 1
        else:
            a_value = self._a._evaluate(point)
            b_value = self._b._evaluate(point)
            self._verify_domain_constraints(a_value, b_value)
            self._value = a_value ** b_value
        return self._value

    def _local_partial(
        self: Power,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        if self._a._lacks_variables and self._a._evaluate(point) == 1:
            # If we find something like, Constant(1) ** Variable("b"), we can short-circuit.
            return 0
        else:
            a_value = self._a._evaluate(point)
            b_value = self._b._evaluate(point)
            self._verify_domain_constraints(a_value, b_value)
            a_partial = self._a._local_partial(point, with_respect_to)
            b_partial = self._b._local_partial(point, with_respect_to)
            # d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db
            return (
                b_value * (a_value ** (b_value - 1)) * a_partial +
                math.log(a_value) * (a_value ** b_value) * b_partial
            )

    def _synthetic_partial(
        self: Power,
        with_respect_to: str
    ) -> sm.Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        b_partial = self._b._synthetic_partial(with_respect_to)
        return ex.Plus(self._term_1(a_partial), self._term_2(b_partial))

    def _compute_local_differential(
        self: Power,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        if self._a._lacks_variables and self._a._evaluate(builder.point) == 1:
            # If we find something like, Constant(1) ** Variable("b"), we can short-circuit.
            pass
        else:
            a_value = self._a._evaluate(builder.point)
            b_value = self._b._evaluate(builder.point)
            self._verify_domain_constraints(a_value, b_value)
            # d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db
            next_accumulated_a = accumulated * b_value * a_value ** (b_value - 1)
            next_accumulated_b = accumulated * math.log(a_value) * a_value ** b_value
            self._a._compute_local_differential(builder, next_accumulated_a)
            self._b._compute_local_differential(builder, next_accumulated_b)

    def _compute_global_differential(
        self: Power,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        self._a._compute_global_differential(builder, self._term_1(accumulated))
        self._b._compute_global_differential(builder, self._term_2(accumulated))

    def _term_1(
        self: Power,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(
            ex.Multiply(self._b, ex.Power(self._a, ex.Minus(self._b, ex.Constant(1)))),
            multiplier
        )

    def _term_2(
        self: Power,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(
            ex.Multiply(ex.Logarithm(math.e, self._a), ex.Power(self._a, self._b)),
            multiplier
        )
