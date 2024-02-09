from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import logarithm, divide, multiply
from smoothmath._private.utilities import is_odd
if TYPE_CHECKING:
    from smoothmath import RealNumber


class Logarithm(base.ParameterizedUnaryExpression):
    """
    A logarithmic expression.

    :param inner: the expression to take the logarithm of
    :param base: the base, as a real number
    """
    def __init__(
        self: Logarithm,
        inner: sm.Expression,
        base: RealNumber = math.e
    ) -> None:
        super().__init__(inner, base)
        if base <= 0:
            raise Exception("Logarithm(x) must have a positive base")
        elif base == 1:
            raise Exception("Logarithm(x) cannot have base = 1")

    @property
    def base(
        self: Logarithm
    ) -> RealNumber:
        return self._parameter

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Logarithm,
        inner_value: RealNumber
    ) -> None:
        if inner_value == 0:
            raise sm.DomainError("Logarithm(x) blows up around x = 0")
        elif inner_value < 0:
            raise sm.DomainError("Logarithm(x) is undefined for x < 0")

    def _value_formula(
        self: Logarithm,
        inner_value: RealNumber
    ):
        return logarithm(inner_value, base = self.base)

    ## Partials and Differentials ##

    def _local_partial_formula(
        self: Logarithm,
        point: sm.Point,
        multiplier: RealNumber
    ) -> RealNumber:
        inner_value = self._inner._evaluate(point)
        if self.base == math.e:
            return divide(multiplier, inner_value)
        else:
            return divide(
                multiplier,
                multiply(logarithm(self.base, base = math.e), inner_value)
            )

    def _synthetic_partial_formula(
        self: Logarithm,
        multiplier: sm.Expression
    ) -> sm.Expression:
        if self.base == math.e:
            return ex.Divide(multiplier, self._inner)
        else:
            return ex.Divide(
                multiplier,
                ex.Multiply(ex.Logarithm(ex.Constant(self.base), base = math.e), self._inner)
            )

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Logarithm
    ) -> list[Callable[[], Optional[sm.Expression]]]:
        return [
            self._reduce_logarithm_of_exponential,
            self._reduce_logarithm_of_reciprocal,
            self._reduce_logarithm_of_nth_power
        ]

    # Logarithm(Exponential(u)) => u
    def _reduce_logarithm_of_exponential(
        self: Logarithm
    ) -> Optional[sm.Expression]:
        if (
            isinstance(self._inner, ex.Exponential) and
            self.base == self._inner.base
        ):
            return self._inner._inner
        else:
            return None

    # Logarithm(Reciprocal(u)) => Negation(Logarithm(u))
    def _reduce_logarithm_of_reciprocal(
        self: Logarithm
    ) -> Optional[sm.Expression]:
        if isinstance(self._inner, ex.Reciprocal):
            return ex.Negation(ex.Logarithm(self._inner._inner, base = self.base))
        else:
            return None

    # Logarithm(NthPower(u, n)) = Multiply(Constant(n), Logarithm(u)) when n is odd
    def _reduce_logarithm_of_nth_power(
        self: Logarithm
    ) -> Optional[sm.Expression]:
        if (
            isinstance(self._inner, ex.NthPower) and
            is_odd(self._inner.n)
        ):
            return ex.Multiply(
                ex.Constant(self._inner.n),
                ex.Logarithm(self._inner._inner, base = self.base)
            )
        else:
            return None
