from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
from smoothmath._private.utilities import integer_from_integral_real_number
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


# differential rule: d(power_N(a)) = N * (power_{N - 1}(a)) * da

class NthPower(base.ParameterizedUnaryExpression):
    def __init__(
        self: NthPower,
        n: int,
        expression: sm.Expression
    ) -> None:
        super().__init__(expression)
        # We want to allow a user to pass a float representation of an integer (e.g. 3.0)
        # even though that wouldn't pass type checking.
        i = integer_from_integral_real_number(n)
        if i is None:
            raise Exception(f"NthPower requires n to be an int, found: {n}")
        self._n: int
        self._n = i

    def _rebuild(
        self: NthPower,
        expression: sm.Expression
    ) -> NthPower:
        return ex.NthPower(self._n, expression)

    def _parameter(
        self: NthPower
    ) -> int:
        return self._n

    def _verify_domain_constraints(
        self: NthPower,
        a_value: sm.real_number,
    ) -> None:
        if a_value == 0:
            if self._n == 0:
                raise sm.DomainError("NthPower(x) is not smooth around x = 0 for n = 0")
            elif self._n <= -1:
                raise sm.DomainError("NthPower(x) blows up around x = 0 when n is negative")

    def _evaluate(
        self: NthPower,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        if self._n == 0:
            self._value = 1
        else: # n is non-zero
            self._value = a_value ** self._n
        return self._value

    def _local_partial(
        self: NthPower,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        a_value = self._a._evaluate(point)
        self._verify_domain_constraints(a_value)
        if self._n == 0:
            return 0
        elif self._n == 1:
            return self._a._local_partial(point, with_respect_to)
        else: # n >= 2 or n <= -1
            a_partial = self._a._local_partial(point, with_respect_to)
            return self._n * nth_power(self._n - 1, a_value) * a_partial

    def _synthetic_partial(
        self: NthPower,
        with_respect_to: str
    ) -> sm.Expression:
        if self._n == 0:
            return ex.Constant(0)
        elif self._n == 1:
            return self._a._synthetic_partial(with_respect_to)
        else: # n >= 2 or n <= -1
            a_partial = self._a._synthetic_partial(with_respect_to)
            return self._synthetic_partial_helper(a_partial)

    def _compute_local_differential(
        self: NthPower,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        a_value = self._a._evaluate(builder.point)
        self._verify_domain_constraints(a_value)
        if self._n == 0:
            return
        elif self._n == 1:
            self._a._compute_local_differential(builder, accumulated)
        else: # n >= 2 or n <= -1
            next_accumulated = accumulated * self._n * nth_power(self._n - 1, a_value)
            self._a._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: NthPower,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        if self._n == 0:
            return
        elif self._n == 1:
            self._a._compute_global_differential(builder, accumulated)
        else: # n >= 2 or n <= -1
            next_accumulated = self._synthetic_partial_helper(accumulated)
            self._a._compute_global_differential(builder, next_accumulated)

    def _local_partial_formula(
        self: NthPower,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        n = self._n
        a_value = self._a._evaluate(point)
        return n * nth_power(n - 1, a_value) * multiplier

    def _synthetic_partial_helper(
        self: NthPower,
        multiplier: sm.Expression
    ) -> sm.Expression:
        n = self._n
        return ex.Multiply(ex.Multiply(ex.Constant(n), ex.NthPower(n - 1, self._a)), multiplier)


def nth_power(
    n: int,
    x: sm.real_number
) -> sm.real_number:
    if x == 0:
        if n == 0:
            raise sm.DomainError("nth_power(x) is not smooth around x = 0 for n = 0")
        elif n <= -1:
            raise sm.DomainError("nth_power(x) blows up around x = 0 when n is negative")
    return x ** n