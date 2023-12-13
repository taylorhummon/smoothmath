from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
from smoothmath._private.utilities import integer_from_integral_real_number
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


def nth_power(
    x: sm.real_number,
    n: int
) -> sm.real_number:
    if x == 0:
        if n == 0:
            raise sm.DomainError("nth_power(x, n) is not smooth around x = 0 for n = 0")
        elif n <= -1:
            raise sm.DomainError("nth_power(x, n) blows up around x = 0 when n is negative")
    return x ** n


class NthPower(base.ParameterizedUnaryExpression):
    def __init__(
        self: NthPower,
        inner: sm.Expression,
        n: int
    ) -> None:
        # We want to allow a user to pass a float representation of an integer (e.g. 3.0)
        # even though that wouldn't pass type checking.
        i = integer_from_integral_real_number(n)
        if i is None:
            raise Exception(f"NthPower requires n to be an int, found: {n}")
        super().__init__(inner, i)

    @property
    def n(
        self: NthPower
    ) -> int:
        return self._parameter

    def _verify_domain_constraints(
        self: NthPower,
        inner_value: sm.real_number
    ) -> None:
        if inner_value == 0:
            if self.n == 0:
                raise sm.DomainError("NthPower(x, n) is not smooth around x = 0 for n = 0")
            elif self.n <= -1:
                raise sm.DomainError("NthPower(x, n) blows up around x = 0 when n is negative")

    def _value_formula(
        self: NthPower,
        inner_value: sm.real_number
    ):
        return nth_power(inner_value, self.n)

    def _local_partial(
        self: NthPower,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        inner_value = self._inner._evaluate(point)
        self._verify_domain_constraints(inner_value)
        if self.n == 0:
            return 0
        else: # n is non-zero
            inner_partial = self._inner._local_partial(point, with_respect_to)
            return self._local_partial_formula(point, inner_partial)

    def _synthetic_partial(
        self: NthPower,
        with_respect_to: str
    ) -> sm.Expression:
        if self.n == 0:
            return ex.Constant(0)
        else: # n is non-zero
            inner_partial = self._inner._synthetic_partial(with_respect_to)
            return self._synthetic_partial_formula(inner_partial)

    def _compute_local_differential(
        self: NthPower,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        inner_value = self._inner._evaluate(builder.point)
        self._verify_domain_constraints(inner_value)
        if self.n == 0:
            return
        else:
            next_accumulated = self._local_partial_formula(builder.point, accumulated)
            self._inner._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: NthPower,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        if self.n == 0:
            return
        else:
            next_accumulated = self._synthetic_partial_formula(accumulated)
            self._inner._compute_global_differential(builder, next_accumulated)

    def _local_partial_formula(
        self: NthPower,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        n = self.n
        if n == 0:
            raise Exception("internal error: n should not be zero here")
        elif n == 1:
            return multiplier
        else:
            inner_value = self._inner._evaluate(point)
            return n * nth_power(inner_value, n - 1) * multiplier

    def _synthetic_partial_formula(
        self: NthPower,
        multiplier: sm.Expression
    ) -> sm.Expression:
        n = self.n
        if n == 0:
            raise Exception("internal error: n should not be zero here")
        elif n == 1:
            return multiplier
        else:
            return ex.Multiply(
                ex.Multiply(ex.Constant(n), ex.NthPower(self._inner, n - 1)),
                multiplier
            )
