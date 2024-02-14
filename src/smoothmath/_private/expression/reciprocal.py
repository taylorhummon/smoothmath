from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import smoothmath._private.base_expression as base
import smoothmath._private.expression as ex
import smoothmath._private.math_functions as mf
import smoothmath._private.errors as er
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression


class Reciprocal(base.UnaryExpression):
    """
    The reciprocal of an expression.

    :param inner: the expression we are taking the reciprocal of
    """

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Reciprocal,
        inner_value: RealNumber
    ) -> None:
        if inner_value == 0:
            raise er.DomainError("Reciprocal(x) blows up around x = 0")

    def _value_formula(
        self: Reciprocal,
        inner_value: RealNumber
    ):
        return mf.reciprocal(inner_value)

    ## Partials ##

    def _local_partial_formula(
        self: Reciprocal,
        point: Point,
        multiplier: RealNumber
    ) -> RealNumber:
        inner_value = self._inner._evaluate(point)
        return mf.negation(mf.divide(multiplier, mf.nth_power(inner_value, n = 2)))

    def _synthetic_partial_formula(
        self: Reciprocal,
        multiplier: Expression
    ) -> Expression:
        return ex.Negation(ex.Divide(multiplier, ex.NthPower(self._inner, n = 2)))

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Reciprocal
    ) -> list[Callable[[], Optional[Expression]]]:
        return [
            self._reduce_reciprocal_of_reciprocal,
            self._reduce_reciprocal_of_negation,
            self._reduce_reciprocal_of_product
        ]

    # Reciprocal(Reciprocal(u)) => u
    def _reduce_reciprocal_of_reciprocal(
        self: Reciprocal
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.Reciprocal):
            return self._inner._inner
        else:
            return None

    # Reciprocal(Negation(u)) => Negation(Reciprocal(u))
    def _reduce_reciprocal_of_negation(
        self: Reciprocal
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.Negation):
            return ex.Negation(ex.Reciprocal(self._inner._inner))
        else:
            return None

    # Reciprocal(Multiply(u, v)) => Multiply(Reciprocal(u), Reciprocal(v))
    def _reduce_reciprocal_of_product(
        self: Reciprocal
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.Multiply):
            return ex.Multiply(*(Reciprocal(inner) for inner in self._inner._inners))
        else:
            return None
