from __future__ import annotations
from typing import Callable
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import nth_power, nth_root, divide, multiply
from smoothmath._private.utilities import integer_from_integral_real_number, is_even, is_odd


class NthRoot(base.ParameterizedUnaryExpression):
    def __init__(
        self: NthRoot,
        inner: sm.Expression,
        n: int
    ) -> None:
        # We want to allow a user to pass a float representation of an integer (e.g. 3.0)
        # even though that wouldn't pass type checking.
        i = integer_from_integral_real_number(n)
        if i is None:
            raise Exception(f"NthRoot() requires parameter n to be an int, found: {n}")
        elif i <= 0:
            raise Exception(f"NthRoot() requires paramater n to be positive, found: {i}")
        super().__init__(inner, i)

    @property
    def n(
        self: NthRoot
    ) -> int:
        return self._parameter

    ## Evaluation ##

    def _verify_domain_constraints(
        self: NthRoot,
        inner_value: sm.real_number
    ) -> None:
        if self.n >= 2 and inner_value == 0:
            raise sm.DomainError(f"NthRoot(x, n) is not defined at x = 0 when n = {self.n}")
        if is_even(self.n) and inner_value < 0:
            raise sm.DomainError(f"NthRoot(x, n) is not defined for negative x when n = {self.n}")

    def _value_formula(
        self: NthRoot,
        inner_value: sm.real_number
    ):
        return nth_root(inner_value, self.n)

    ## Partials and Differentials ##

    def _local_partial_formula(
        self: NthRoot,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        n = self.n
        if n == 1:
            return multiplier
        else:
            self_value = self._evaluate(point)
            return divide(
                multiplier,
                multiply(n, nth_power(self_value, n - 1))
            )

    def _synthetic_partial_formula(
        self: NthRoot,
        multiplier: sm.Expression
    ) -> sm.Expression:
        n = self.n
        if n == 1:
            return multiplier
        else: # n >= 2
            return ex.Divide(
                multiplier,
                ex.Multiply(ex.Constant(n), ex.NthPower(self, n - 1))
            )

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: NthRoot
    ) -> list[Callable[[], sm.Expression | None]]:
        return [
            self._reduce_nth_root_where_n_is_one,
            self._reduce_nth_root_of_mth_power,
            self._reduce_nth_root_of_mth_root,
            self._reduce_odd_nth_root_of_negation,
            self._reduce_nth_root_of_reciprocal
        ]

    # NthRoot(u, 1) => u
    def _reduce_nth_root_where_n_is_one(
        self: NthRoot
    ) -> sm.Expression | None:
        if self.n == 1:
            return self._inner
        else:
            return None

    # NthRoot(NthPower(u, m), n) => NthPower(NthRoot(u, n), m)
    def _reduce_nth_root_of_mth_power(
        self: NthRoot
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.NthPower):
            return ex.NthPower(
                ex.NthRoot(self._inner._inner, self.n),
                self._inner.n
            )
        else:
            return None

    # NthRoot(NthRoot(u, m), n) => NthRoot(u, m * n))
    def _reduce_nth_root_of_mth_root(
        self: NthRoot
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.NthRoot):
            return ex.NthRoot(self._inner._inner, self.n * self._inner.n)
        else:
            return None

    # NthRoot(Negation(u), n) => Negation(NthRoot(u, n)) where n is odd
    def _reduce_odd_nth_root_of_negation(
        self: NthRoot
    ) -> sm.Expression | None:
        if (
            isinstance(self._inner, ex.Negation) and
            is_odd(self.n)
        ):
            return ex.Negation(ex.NthRoot(self._inner._inner, self.n))
        else:
            return None

    # NthRoot(Reciprocal(u), n) => Reciprocal(NthRoot(u, n))
    def _reduce_nth_root_of_reciprocal(
        self: NthRoot
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.Reciprocal):
            return ex.Reciprocal(ex.NthRoot(self._inner._inner, self.n))
        else:
            return None
