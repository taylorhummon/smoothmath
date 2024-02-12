from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import math
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
import smoothmath._private.math_functions as mf
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression


class Exponential(base.ParameterizedUnaryExpression):
    """
    An exponential expression.

    :param inner: the exponent
    :param base: the base, as a real number
    """

    def __init__(
        self: Exponential,
        inner: Expression,
        base: RealNumber = math.e
    ) -> None:
        super().__init__(inner, base)
        if base <= 0:
            raise Exception(f"Exponential(x) must have a positive base, found: {base}")

    @property
    def base(
        self: Exponential
    ) -> RealNumber:
        return self._parameter

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Exponential,
        inner_value: RealNumber
    ) -> None:
        pass

    def _value_formula(
        self: Exponential,
        inner_value: RealNumber
    ):
        return mf.exponential(inner_value, base = self.base)

    ## Partials and Differentials ##

    def _local_partial_formula(
        self: Exponential,
        point: Point,
        multiplier: RealNumber
    ) -> RealNumber:
        if self.base == 1:
            return 0
        self_value = self._evaluate(point)
        if self.base == math.e:
            return mf.multiply(self_value, multiplier)
        else:
            return mf.multiply(
                mf.logarithm(self.base, base = math.e),
                self_value,
                multiplier
            )

    def _synthetic_partial_formula(
        self: Exponential,
        multiplier: Expression
    ) -> Expression:
        if self.base == 1:
            return ex.Constant(0)
        elif self.base == math.e:
            return ex.Multiply(self, multiplier)
        else:
            return ex.Multiply(
                ex.Logarithm(ex.Constant(self.base), base = math.e),
                self,
                multiplier
            )

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Exponential
    ) -> list[Callable[[], Optional[Expression]]]:
        return [
            self._reduce_exponential_of_logarithm,
            self._reduce_exponential_of_negation
        ]

    # Exponential(Logarithm(u)) => u
    def _reduce_exponential_of_logarithm(
        self: Exponential
    ) -> Optional[Expression]:
        if (
            isinstance(self._inner, ex.Logarithm) and
            self.base == self._inner.base
        ):
            return self._inner._inner
        else:
            return None

    # Exponential(Negation(u)) => Reciprocal(Exponential(u))
    def _reduce_exponential_of_negation(
        self: Exponential
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.Negation):
            return ex.Reciprocal(ex.Exponential(self._inner._inner, base = self.base))
        else:
            return None
