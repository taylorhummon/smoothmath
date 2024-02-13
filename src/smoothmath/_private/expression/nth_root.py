from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import smoothmath._private.base_expression as base
import smoothmath._private.expression as ex
import smoothmath._private.math_functions as mf
import smoothmath._private.utilities as util
import smoothmath._private.errors as er
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression


class NthRoot(base.ParameterizedUnaryExpression):
    """
    The nth root of an expression.

    :param inner: the expression we are taking the nth root of
    :param n: *must be an integer greater or equal to 1*; use n = 2 for square root
    """

    def __init__(
        self: NthRoot,
        inner: Expression,
        n: int
    ) -> None:
        # We want to allow a user to pass a float representation of an integer (e.g. 3.0)
        # even though that wouldn't pass type checking.
        i = util.integer_from_integral_real_number(n)
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
        inner_value: RealNumber
    ) -> None:
        if self.n >= 2 and inner_value == 0:
            raise er.DomainError(f"NthRoot(x, n) is not defined at x = 0 when n = {self.n}")
        if util.is_even(self.n) and inner_value < 0:
            raise er.DomainError(f"NthRoot(x, n) is not defined for negative x when n = {self.n}")

    def _value_formula(
        self: NthRoot,
        inner_value: RealNumber
    ):
        return mf.nth_root(inner_value, self.n)

    ## Partials and Differentials ##

    def _local_partial_formula(
        self: NthRoot,
        point: Point,
        multiplier: RealNumber
    ) -> RealNumber:
        n = self.n
        if n == 1:
            return multiplier
        else:
            self_value = self._evaluate(point)
            return mf.divide(
                multiplier,
                mf.multiply(n, mf.nth_power(self_value, n - 1))
            )

    def _synthetic_partial_formula(
        self: NthRoot,
        multiplier: Expression
    ) -> Expression:
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
    ) -> list[Callable[[], Optional[Expression]]]:
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
    ) -> Optional[Expression]:
        if self.n == 1:
            return self._inner
        else:
            return None

    # NthRoot(NthPower(u, m), n) => NthPower(NthRoot(u, n), m)
    def _reduce_nth_root_of_mth_power(
        self: NthRoot
    ) -> Optional[Expression]:
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
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.NthRoot):
            return ex.NthRoot(self._inner._inner, self.n * self._inner.n)
        else:
            return None

    # NthRoot(Negation(u), n) => Negation(NthRoot(u, n)) where n is odd
    def _reduce_odd_nth_root_of_negation(
        self: NthRoot
    ) -> Optional[Expression]:
        if (
            isinstance(self._inner, ex.Negation) and
            util.is_odd(self.n)
        ):
            return ex.Negation(ex.NthRoot(self._inner._inner, self.n))
        else:
            return None

    # NthRoot(Reciprocal(u), n) => Reciprocal(NthRoot(u, n))
    def _reduce_nth_root_of_reciprocal(
        self: NthRoot
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.Reciprocal):
            return ex.Reciprocal(ex.NthRoot(self._inner._inner, self.n))
        else:
            return None
