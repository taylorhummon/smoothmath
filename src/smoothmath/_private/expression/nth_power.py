from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import math
import smoothmath._private.base_expression as base
import smoothmath._private.expression as ex
import smoothmath._private.math_functions as mf
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression


class NthPower(base.ParameterizedUnaryExpression):
    """
    The nth power of an expression.

    >>> from smoothmath.expression import Variable, NthPower
    >>> NthPower(Variable("x"), n=2).at(3)
    9.0

    :param inner: the expression being raised to the nth power
    :param n: the exponent, *which must be an integer greater or equal to 1*
    """

    def __init__(
        self: NthPower,
        inner: Expression,
        n: int
    ) -> None:
        # We want to allow a user to pass a float representation of an integer (e.g. 3.0)
        # even though that wouldn't pass type checking.
        i = util.integer_from_integral_real_number(n)
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
        inner_value: RealNumber
    ) -> None:
        pass

    def _value_formula(
        self: NthPower,
        inner_value: RealNumber
    ):
        return mf.nth_power(inner_value, self.n)

    ## Partials ##

    def _numeric_partial_formula(
        self: NthPower,
        point: Point,
        multiplier: RealNumber
    ) -> RealNumber:
        n = self.n
        if n == 1:
            return multiplier
        else: # n >= 2
            inner_value = self._inner._evaluate(point)
            return mf.multiply(
                n,
                mf.nth_power(inner_value, n - 1),
                multiplier
            )

    def _synthetic_partial_formula(
        self: NthPower,
        multiplier: Expression
    ) -> Expression:
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
    ) -> list[Callable[[], Optional[Expression]]]:
        return [
            self._reduce_nth_power_where_n_is_one,
            self._reduce_nth_power_of_mth_root,
            self._reduce_nth_power_of_mth_power,
            self._reduce_nth_power_of_negation,
            self._reduce_nth_power_of_reciprocal,
            self._reduce_nth_power_of_exponential
        ]

    # NthPower(u, 1) => u
    def _reduce_nth_power_where_n_is_one(
        self: NthPower
    ) -> Optional[Expression]:
        if self.n == 1:
            return self._inner
        else:
            return None

    # NthPower(NthRoot(u, m), n) => ...
    def _reduce_nth_power_of_mth_root(
        self: NthPower
    ) -> Optional[Expression]:
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
    def _reduce_nth_power_of_mth_power(
        self: NthPower
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.NthPower):
            return ex.NthPower(self._inner._inner, self.n * self._inner.n)
        else:
            return None

    # NthPower(Negation(u), n) => NthPower(u, n) when n is even
    # NthPower(Negation(u), n) => Negation(NthPower(u, n)) when n is odd
    def _reduce_nth_power_of_negation(
        self: NthPower
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.Negation):
            if util.is_even(self.n):
                return ex.NthPower(self._inner._inner, self.n)
            else: # n is odd
                return ex.Negation(ex.NthPower(self._inner._inner, self.n))
        else:
            return None

    # NthPower(Reciprocal(u), n) => Reciprocal(NthPower(u, n))
    def _reduce_nth_power_of_reciprocal(
        self: NthPower
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.Reciprocal):
            return ex.Reciprocal(ex.NthPower(self._inner._inner, self.n))
        else:
            return None

    # NthPower(Exponential(u), n) => Exponential(Multiply(Constant(n), u))
    def _reduce_nth_power_of_exponential(
        self: NthPower
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.Exponential):
            return ex.Exponential(
                ex.Multiply(ex.Constant(self.n), self._inner._inner),
                base = self._inner.base
            )
        else:
            return None
