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
    if n <= 0:
        raise sm.DomainError(f"nth_power(x, n) is not defined for n = {n}")
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
            raise Exception(f"NthPower() requires n to be an int, found: {n}")
        elif i <= 0:
            raise Exception(f"NthPower() requires n to be positive, found: {i}")
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
        pass

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
        inner_partial = self._inner._local_partial(point, with_respect_to)
        return self._local_partial_formula(point, inner_partial)

    def _synthetic_partial(
        self: NthPower,
        with_respect_to: str
    ) -> sm.Expression:
        inner_partial = self._inner._synthetic_partial(with_respect_to)
        return self._synthetic_partial_formula(inner_partial)

    def _compute_local_differential(
        self: NthPower,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        inner_value = self._inner._evaluate(builder.point)
        self._verify_domain_constraints(inner_value)
        next_accumulated = self._local_partial_formula(builder.point, accumulated)
        self._inner._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: NthPower,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_formula(accumulated)
        self._inner._compute_global_differential(builder, next_accumulated)

    def _local_partial_formula(
        self: NthPower,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        n = self.n
        if n == 1:
            return multiplier
        else: # n >= 2
            inner_value = self._inner._evaluate(point)
            return n * nth_power(inner_value, n - 1) * multiplier

    def _synthetic_partial_formula(
        self: NthPower,
        multiplier: sm.Expression
    ) -> sm.Expression:
        n = self.n
        if n == 1:
            return multiplier
        else: # n >= 2
            return ex.Multiply(
                ex.Multiply(ex.Constant(n), ex.NthPower(self._inner, n - 1)),
                multiplier
            )
