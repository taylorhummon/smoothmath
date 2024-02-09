from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import negation, minus
if TYPE_CHECKING:
    from smoothmath import RealNumber
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Minus(base.BinaryExpression):
    """
    Subtraction.

    :param left: the expression being subtracted from
    :param right: the expression being subtracted
    """

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Minus,
        left_value: RealNumber,
        right_value: RealNumber
    ) -> None:
        pass

    def _value_formula(
        self: Minus,
        left_value: RealNumber,
        right_value: RealNumber
    ) -> RealNumber:
        return minus(left_value, right_value)

    ## Partials and Differentials ##

    def _local_partial(
        self: Minus,
        point: sm.Point,
        variable: str
    ) -> RealNumber:
        left_partial = self._left._local_partial(point, variable)
        right_partial = self._right._local_partial(point, variable)
        return minus(left_partial, right_partial)

    def _synthetic_partial(
        self: Minus,
        variable: str
    ) -> sm.Expression:
        left_partial = self._left._synthetic_partial(variable)
        right_partial = self._right._synthetic_partial(variable)
        return ex.Minus(left_partial, right_partial)

    def _compute_local_differential(
        self: Minus,
        builder: LocalDifferentialBuilder,
        accumulated: RealNumber
    ) -> None:
        self._left._compute_local_differential(builder, accumulated)
        self._right._compute_local_differential(builder, negation(accumulated))

    def _compute_global_differential(
        self: Minus,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        self._left._compute_global_differential(builder, accumulated)
        self._right._compute_global_differential(builder, ex.Negation(accumulated))

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Minus
    ) -> list[Callable[[], Optional[sm.Expression]]]:
        return [self._reduce_minus_to_sum_with_negation]

    # Minus(u, v) => Add(u, Negation(v))
    def _reduce_minus_to_sum_with_negation(
        self: Minus
    ) -> Optional[sm.Expression]:
        return ex.Add(self._left, ex.Negation(self._right))
