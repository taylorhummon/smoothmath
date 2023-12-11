from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Plus(base.BinaryExpression):
    def __init__(
        self: Plus,
        left: sm.Expression,
        right: sm.Expression
    ) -> None:
        super().__init__(left, right)

    def _evaluate(
        self: Plus,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        left_value = self._left._evaluate(point)
        right_value = self._right._evaluate(point)
        self._value = left_value + right_value
        return self._value

    def _local_partial(
        self: Plus,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        left_partial = self._left._local_partial(point, with_respect_to)
        right_partial = self._right._local_partial(point, with_respect_to)
        return left_partial + right_partial

    def _synthetic_partial(
        self: Plus,
        with_respect_to: str
    ) -> sm.Expression:
        left_partial = self._left._synthetic_partial(with_respect_to)
        right_partial = self._right._synthetic_partial(with_respect_to)
        return ex.Plus(left_partial, right_partial)

    def _compute_local_differential(
        self: Plus,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        self._left._compute_local_differential(builder, accumulated)
        self._right._compute_local_differential(builder, accumulated)

    def _compute_global_differential(
        self: Plus,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        self._left._compute_global_differential(builder, accumulated)
        self._right._compute_global_differential(builder, accumulated)
