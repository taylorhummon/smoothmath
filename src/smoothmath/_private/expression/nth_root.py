from __future__ import annotations
from typing import TYPE_CHECKING
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
from smoothmath._private.expression.nth_power import nth_power
from smoothmath._private.utilities import integer_from_integral_real_number
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


def nth_root(
    n: int,
    x: sm.real_number
) -> sm.real_number:
    if n <= 0:
        raise sm.DomainError(f"nth_root(x) is not defined when n = {n}")
    if n >= 2 and x == 0:
        raise sm.DomainError(f"nth_root(x) is not defined at x = 0 when n = {n}")
    if n % 2 == 0 and x < 0:
        raise sm.DomainError(f"nth_root(x) is not defined for negative x when n = {n}")
    if n == 1:
        return x
    if n == 2:
        return math.sqrt(x)
    elif n == 3:
        return math.cbrt(x)
    else:
        return x ** (1 / n)


class NthRoot(base.ParameterizedUnaryExpression):
    def __init__(
        self: NthRoot,
        n: int,
        inner: sm.Expression
    ) -> None:
        super().__init__(inner)
        # We want to allow a user to pass a float representation of an integer (e.g. 3.0)
        # even though that wouldn't pass type checking.
        i = integer_from_integral_real_number(n)
        if i is None:
            raise Exception(f"NthRoot requires n to be an int, found: {n}")
        elif i <= 0:
            raise Exception(f"NthRoot needs n to be positive, found {i}")
        self._n: int
        self._n = i

    def _parameter(
        self: NthRoot
    ) -> int:
        return self._n

    def _verify_domain_constraints(
        self: NthRoot,
        inner_value: sm.real_number
    ) -> None:
        if self._n >= 2 and inner_value == 0:
            raise sm.DomainError(f"NthRoot(x) is not defined at x = 0 when n = {self._n}")
        if self._n % 2 == 0 and inner_value < 0:
            raise sm.DomainError(f"NthRoot(x) is not defined for negative x when n = {self._n}")

    def _value_formula(
        self: NthRoot,
        inner_value: sm.real_number
    ):
        return nth_root(self._n, inner_value)

    def _local_partial(
        self: NthRoot,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        inner_value = self._inner._evaluate(point)
        self._verify_domain_constraints(inner_value)
        inner_partial = self._inner._local_partial(point, with_respect_to)
        return self._local_partial_formula(point, inner_partial)

    def _synthetic_partial(
        self: NthRoot,
        with_respect_to: str
    ) -> sm.Expression:
        inner_partial = self._inner._synthetic_partial(with_respect_to)
        return self._synthetic_partial_formula(inner_partial)

    def _compute_local_differential(
        self: NthRoot,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        inner_value = self._inner._evaluate(builder.point)
        self._verify_domain_constraints(inner_value)
        next_accumulated = self._local_partial_formula(builder.point, accumulated)
        self._inner._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: NthRoot,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_formula(accumulated)
        self._inner._compute_global_differential(builder, next_accumulated)

    def _local_partial_formula(
        self: NthRoot,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        n = self._n
        if n == 1:
            return multiplier
        else:
            self_value = self._evaluate(point)
            return multiplier / (n * (nth_power(n - 1, self_value)))

    def _synthetic_partial_formula(
        self: NthRoot,
        multiplier: sm.Expression
    ) -> sm.Expression:
        n = self._n
        if n == 1:
            return multiplier
        else: # n >= 2
            return ex.Divide(multiplier, ex.Multiply(ex.Constant(n), ex.NthPower(n - 1, self)))
