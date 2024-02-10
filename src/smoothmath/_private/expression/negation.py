from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import negation
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression


class Negation(base.UnaryExpression):
    """
    The opposite (negative) of an expression.

    :param inner: the inner expression
    """

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Negation,
        inner_value: RealNumber
    ) -> None:
        pass

    def _value_formula(
        self: Negation,
        inner_value: RealNumber
    ) -> RealNumber:
        return negation(inner_value)

    ## Partials and Differentials ##

    def _local_partial_formula(
        self: Negation,
        point: Point,
        multiplier: RealNumber
    ) -> RealNumber:
        return negation(multiplier)

    def _synthetic_partial_formula(
        self: Negation,
        multiplier: Expression
    ) -> Expression:
        return ex.Negation(multiplier)

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Negation
    ) -> list[Callable[[], Optional[Expression]]]:
        return [
            self._reduce_negation_of_negation,
            self._reduce_negation_of_sum
        ]

    # Negation(Negation(u)) => u
    def _reduce_negation_of_negation(
        self: Negation
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.Negation):
            return self._inner._inner
        else:
            return None

    # Negation(Add(u, v)) => Add(Negation(u), Negation(v))
    def _reduce_negation_of_sum(
        self: Negation
    ) -> Optional[Expression]:
        if isinstance(self._inner, ex.Add):
            return ex.Add(*(Negation(inner) for inner in self._inner._inners))
        else:
            return None
