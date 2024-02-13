from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import smoothmath._private.base_expression as base
import smoothmath._private.expression as ex
import smoothmath._private.math_functions as mf
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression


class Cosine(base.UnaryExpression):
    """
    The cosine of an expression.

    :param inner: an expression representing an angle in radians
    """

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Cosine,
        inner_value: RealNumber
    ) -> None:
        pass

    def _value_formula(
        self: Cosine,
        inner_value: RealNumber
    ) -> RealNumber:
        return mf.cosine(inner_value)

    ## Partials and Differentials ##

    def _local_partial_formula(
        self: Cosine,
        point: Point,
        multiplier: RealNumber
    ) -> RealNumber:
        inner_value = self._inner._evaluate(point)
        return mf.multiply(mf.negation(mf.sine(inner_value)), multiplier)

    def _synthetic_partial_formula(
        self: Cosine,
        multiplier: Expression
    ) -> Expression:
        return ex.Multiply(ex.Negation(ex.Sine(self._inner)), multiplier)

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Cosine
    ) -> list[Callable[[], Optional[Expression]]]:
        return [self._reduce_cosine_of_negation]

    # Cosine(Negation(u)) => Cosine(u)
    def _reduce_cosine_of_negation(
        self: Cosine
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.Negation):
            return ex.Cosine(self._inner._inner)
        else:
            return None
