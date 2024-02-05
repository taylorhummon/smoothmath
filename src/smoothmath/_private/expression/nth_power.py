from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import nth_power, multiply
from smoothmath._private.utilities import integer_from_integral_real_number, is_even
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


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
            raise Exception(f"NthPower() requires parameter n to be an int, found: {n}")
        elif i <= 0:
            raise Exception(f"NthPower() requires parameter n to be positive, found: {i}")
        super().__init__(inner, i)

    @property
    def n(
        self: NthPower
    ) -> int:
        return self._parameter

    ## Evaluation ##

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

    ## Partials and Differentials ##

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
            return multiply(
                n,
                nth_power(inner_value, n - 1),
                multiplier
            )

    def _synthetic_partial_formula(
        self: NthPower,
        multiplier: sm.Expression
    ) -> sm.Expression:
        n = self.n
        if n == 1:
            return multiplier
        else: # n >= 2
            return ex.Multiply(
                ex.Constant(n),
                ex.NthPower(self._inner, n - 1),
                multiplier
            )

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: NthPower
    ) -> list[Callable[[], sm.Expression | None]]:
        return [
            self._reduce_nth_power_where_n_is_one,
            self._reduce_nth_power_of_mth_root_of_u,
            self._reduce_nth_power_of_mth_power_of_u,
            self._reduce_nth_power_of_negation_of_u,
            self._reduce_nth_power_of_reciprocal_of_u,
            self._reduce_nth_power_of_exponential_of_u
        ]

    # NthPower(u, 1) => u
    def _reduce_nth_power_where_n_is_one(
        self: NthPower
    ) -> sm.Expression | None:
        if self.n == 1:
            return self._inner
        else:
            return None

    # NthPower(NthRoot(u, m), n) => ...
    def _reduce_nth_power_of_mth_root_of_u(
        self: NthPower
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.NthRoot):
            n = self.n
            m = self._inner.n
            if m == n:
                return self._inner._inner
            greatest_common_divisor = math.gcd(m, n)
            if greatest_common_divisor != 1:
                return ex.NthPower(
                    ex.NthRoot(self._inner._inner, m // greatest_common_divisor),
                    n // greatest_common_divisor
                )
        else:
            return None

    # NthPower(NthPower(u, m), n) => NthPower(u, m * n))
    def _reduce_nth_power_of_mth_power_of_u(
        self: NthPower
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.NthPower):
            return ex.NthPower(self._inner._inner, self.n * self._inner.n)
        else:
            return None

    # NthPower(Negation(u), n) => NthPower(u, n) when n is even
    # NthPower(Negation(u), n) => Negation(NthPower(u, n)) when n is odd
    def _reduce_nth_power_of_negation_of_u(
        self: NthPower
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.Negation):
            if is_even(self.n):
                return ex.NthPower(self._inner._inner, self.n)
            else: # n is odd
                return ex.Negation(ex.NthPower(self._inner._inner, self.n))
        else:
            return None

    # NthPower(Reciprocal(u), n) => Reciprocal(NthPower(u, n))
    def _reduce_nth_power_of_reciprocal_of_u(
        self: NthPower
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.Reciprocal):
            return ex.Reciprocal(ex.NthPower(self._inner._inner, self.n))
        else:
            return None

    # NthPower(Exponential(u), n) => Exponential(Multiply(Constant(n), u))
    def _reduce_nth_power_of_exponential_of_u(
        self: NthPower
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.Exponential):
            return ex.Exponential(
                ex.Multiply(ex.Constant(self.n), self._inner._inner),
                base = self._inner.base
            )
        else:
            return None
