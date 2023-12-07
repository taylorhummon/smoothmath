from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


# differential rule: d(a + b) = da + db

class Plus(base.BinaryExpression):
    def __init__(
        self: Plus,
        a: sm.Expression,
        b: sm.Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Plus,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        b_value = self._b._evaluate(point)
        self._value = a_value + b_value
        return self._value

    def _local_partial(
        self: Plus,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        a_partial = self._a._local_partial(point, with_respect_to)
        b_partial = self._b._local_partial(point, with_respect_to)
        return a_partial + b_partial

    def _synthetic_partial(
        self: Plus,
        with_respect_to: str
    ) -> sm.Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        b_partial = self._b._synthetic_partial(with_respect_to)
        return ex.Plus(a_partial, b_partial)

    def _compute_local_differential(
        self: Plus,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        self._a._compute_local_differential(builder, accumulated)
        self._b._compute_local_differential(builder, accumulated)

    def _compute_global_differential(
        self: Plus,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        self._a._compute_global_differential(builder, accumulated)
        self._b._compute_global_differential(builder, accumulated)
